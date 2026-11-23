// The runner for shipping-rules.md. It holds the logic; the markdown file holds the cases.
import { readFileSync } from 'node:fs';
import * as v from 'valibot';
import { describe, expect, expectTypeOf, test } from 'vitest';
import { shippingFee, type Cart, type Destination } from '../src/shipping.ts';
import { readMarkdownTables } from './harness/markdown-tables.ts';

// `as const` lists, so the coverage test can compare them with the union at the type level.
const KINDS = ['pickup', 'domestic', 'abroad'] as const;
const ZONES = ['eu', 'world'] as const;
const YES_NO = v.pipe(v.picklist(['yes', 'no']), v.transform((cell) => cell === 'yes'));
const EUROS = v.pipe(v.string(), v.regex(/^[0-9]+$/), v.transform(Number));

const tables = readMarkdownTables(readFileSync(new URL('shipping-rules.md', import.meta.url), 'utf8'));

/** `domestic · express yes`: the destination that every row of the section shares. */
function sectionOf(heading: string): Destination {
  const [kindText, ...parts] = heading.split(' · ');
  const kind = v.parse(v.picklist(KINDS), kindText);
  const valueOf = (key: string) => parts.find((part) => part.startsWith(`${key} `))?.slice(key.length + 1);
  const unknown = parts.filter((part) => !/^(express|zone) /.test(part));
  if (unknown.length > 0) throw new Error(`unknown part of "${heading}": ${unknown.join(', ')}`);
  switch (kind) {
    case 'pickup':
      if (parts.length > 0) throw new Error(`a pickup takes no option: ${heading}`);
      return { kind };
    case 'domestic':
      return { kind, express: v.parse(YES_NO, valueOf('express')) };
    case 'abroad':
      return { kind, zone: v.parse(v.picklist(ZONES), valueOf('zone')) };
    default: {
      const _exhaustive: never = kind;
      return _exhaustive;
    }
  }
}

/** `subtotal 50, battery`: how the cart differs from the usual cart. An unknown word fails. */
function cartOf(is: string): Cart {
  let cart: Cart = { subtotal: 20, battery: false };
  for (const trait of is === '' ? [] : is.split(', ')) {
    const subtotal = /^subtotal ([0-9]+)$/.exec(trait);
    if (subtotal !== null) cart = { ...cart, subtotal: Number(subtotal[1]) };
    else if (trait === 'battery') cart = { ...cart, battery: true };
    else throw new Error(`unknown trait "${trait}" in "${is}"`);
  }
  return cart;
}

// Strict: a missing or extra column fails, so every answer is required.
const FeeRowSchema = v.strictObject({
  case: v.pipe(v.string(), v.nonEmpty()),
  'cart is': v.string(),
  fee: v.union([v.pipe(v.literal('none'), v.transform(() => null)), EUROS]),
  refused: YES_NO,
});

const feeRows = tables
  .filter(({ part }) => part === 'Fees')
  .flatMap(({ section, rows }) => {
    const destination = sectionOf(section);
    return v.parse(v.array(FeeRowSchema), rows).map((row) => ({
      name: `${row.case} · ${section}`,
      destination,
      cart: cartOf(row['cart is']),
      expected: { fee: row.fee, refused: row.refused },
    }));
  });

describe('the rules of the shipping fee', () => {
  test('every kind of destination has a row', () => {
    // A new kind of destination fails tsc here, then this test until it gets a row.
    expectTypeOf<(typeof KINDS)[number]>().toEqualTypeOf<Destination['kind']>();
    expect(new Set(feeRows.map(({ destination }) => destination.kind))).toEqual(new Set(KINDS));
  });

  // One toEqual on all the answers: a red row shows every answer that is wrong.
  test.each(feeRows)('$name', ({ destination, cart, expected }) => {
    const fee = shippingFee({ cart, destination });
    expect({ fee: fee.kind === 'refused' ? null : fee.euros, refused: fee.kind === 'refused' }).toEqual(expected);
  });
});
