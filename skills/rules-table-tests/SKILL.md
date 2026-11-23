---
name: rules-table-tests
description: "Write or migrate tests as a rules table: a markdown file of cases that a generic runner reads (tests as data). Use when a pure rule or decision needs many stateless cases, when the user asks for tests as data or table tests, or to move an existing test file of repeated cases into that shape."
license: MIT
---

# Rules table tests

A **rules table** is a markdown file that a person reads as the spec of a rule, and that a test
runs row by row. The file holds the cases and the reasons. The runner holds the logic. Based on
[Tests as data](https://martinfowler.com/articles/tests-as-data.html).

The worked example is a shipping fee, in TypeScript with vitest and valibot:
[`agents/shipping-rules.md`](agents/shipping-rules.md) (the data) and
[`agents/shipping.test.ts`](agents/shipping.test.ts) (the runner), for the code in
[`agents/shipping.ts`](agents/shipping.ts). Read the data and the runner before you
write a table. In another language, keep the principles and translate the code.

## When it fits

The code under test is a pure decision: a few inputs in, an answer out, no state between cases. The
cases share a context (the same destination, the same config) and differ in one or two things. Keep
integration tests, snapshot tests and tests of effects in code: a table cannot show a call order.

## Steps

1. **Pin.** Migration: run the old tests green, and list every case they assert. New tests: list
   the rules of the code, each with the input that shows it and the input on its border. Done when
   each rule has a case and each border (the threshold, the first and the last value, an empty list)
   has one.
2. **Write the file** `<module>-rules.md` next to the test, in the shape below. Done when every
   sentence of the file passes the [STE rules](#write-in-ste), and each term in the rows is in
   *Terms*.
3. **Write the runner** in the test file, as in [Runner](#runner). For a TypeScript project, copy
   [`agents/markdown-tables.ts`](agents/markdown-tables.ts) to the test harness folder,
   unless the project has a table reader already.
4. **Prove each rule.** Break each rule in the code once (change one condition, one number, one
   string). Run the table: the row for that rule goes red, with an assertion diff on that answer.
   Put the code back. Done when every rule turned a row red, and the code under test has no change.
5. **Migration: delete the old cases** the table now covers, in the same commit. Keep a test that
   is not a stateless case.
6. Run the test file and the type check. Report the case count and the result of each break.

## The file

```markdown
# The rules of <concept>

<Two sentences: what the code decides, and that `<module>.test.ts` runs every row.>

## Why these rules exist
<The spirit: the problem each rule solves for the user, the cost when it is wrong, the cases the
rule never touches, what it does when it does not know.>

## Terms
<Each domain term the rows use, one line each, and a pointer to the project glossary if it has one.>

## How to read this file
<Each part of a heading, each column, the usual case, each word a "differs" cell can hold.>

# <Answers>            <- one `#` part per function or per set of answers

## <kind> · <key> <value> · <key> <value>     <- the context that the rows share

<Optional: one or two sentences on why these answers.>

| case                 | <input> is  | <answer> | <answer> |
|----------------------|-------------|----------|----------|
| <one rule, in words> | subtotal 50 | 0        | no       |
```

- **Context in the heading.** What all rows share goes in the `##` heading as `·` parts, never in
  a column repeated on each row. One heading per variant of the input union.
- **Rows give only the difference.** The intro names the usual case. An `<input> is` cell holds the
  words that change it (`subtotal 50, battery`), empty for the usual case.
- **Answers are columns**, each one required: `yes`/`no`, a number, or exact text in backticks.
  `none` for an absent answer.
- **A case name is one rule**, with the terms of the intro: "an express cart at the free
  subtotal". Unique in its section. The test name starts with it.
- **Prose is comment.** Text outside tables is for people. The runner reads headings and tables only.
- Align the columns. A cell holds no `|`. Prefer markdown to CSV: code hosts and editors render
  it, and a heading holds the shared context that CSV repeats on every row.

## Write in STE

The rules file is the spec of the rule: a reader with no context must understand each rule the
first time. Write all its prose in Simplified Technical English (ASD-STE100): the intro, *Why these
rules exist*, *Terms*, *How to read this file*, the text under each heading, and the case names.
The table cells are data words, not sentences.

- One idea per sentence. Split a sentence at "and", "but" or ":" when a second idea follows.
- Use the active voice: "the shop refuses the order", not "the order is refused".
- Use simple tenses: the present, the simple past, the future.
- Keep a sentence to 20 words or fewer.
- Use one term for one concept. Take it from *Terms*, and keep it everywhere, the rows included.
- Keep the articles: "the order", "a cart".
- Keep a noun cluster to 3 words or fewer: "the fee of a domestic delivery", not "domestic delivery
  base fee".
- Give the reason after the rule, in its own sentence: "Thus …".

## Runner

Each principle, then how the TypeScript example does it.

- **One generic reader.** It turns the file into `{ part, section, rows }`, each row a record keyed
  by the header. The runner filters by `part`. (`readMarkdownTables`.)
- **Refuse what it does not understand.** An unknown heading part, an unknown word in a cell, a
  missing or extra column: each one throws, so a typo fails instead of passing. (`sectionOf`,
  `cartOf`, valibot `strictObject`.)
- **Parse cells at the edge.** Each cell becomes a domain value before the test runs: `yes` becomes
  `true`, `none` becomes `null`, `subtotal 50` becomes a cart. (valibot `pipe` and `transform`.)
- **Exhaust the variants.** The runner builds each variant of the input union in one switch that
  fails to compile when a variant is missing, with no type cast. (A `never` arm, no `as`.)
- **Cover every variant.** A test fails while a variant of the input has no row, and the type
  checker fails when the list of variants drifts from the type. (`expectTypeOf<(typeof
  KINDS)[number]>().toEqualTypeOf<Destination['kind']>()`, then the set of kinds in the rows
  equal to `KINDS`.)
- **Name each test from its row.** The case first, then the section, so a red test reads as the
  broken rule. (``test.each(rows)('$name', …)`` with ``name: `${row.case} · ${section}` ``.)
- **Compare all the answers at once.** One equality on an object of every answer, so a red row
  shows each answer that is wrong. (One `toEqual`.)
