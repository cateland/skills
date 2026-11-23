/** A markdown table and the `#` and `##` headings it sits under. */
export type MarkdownTable = {
  readonly part: string;
  readonly section: string;
  readonly rows: readonly Readonly<Record<string, string>>[];
};

/**
 * The tables of a markdown file, each row a record keyed by its table's header. A cell is trimmed,
 * one pair of enclosing backticks removed. A cell cannot hold a `|`. Prose between tables is a comment.
 */
export function readMarkdownTables(text: string): readonly MarkdownTable[] {
  const tables: { part: string; section: string; lines: string[] }[] = [];
  let part = '';
  let section = '';
  let inTable = false;
  for (const line of text.split('\n')) {
    const heading = /^(#{1,2}) (.*)$/.exec(line);
    if (heading !== null) [part, section] = heading[1] === '#' ? [heading[2] ?? '', ''] : [part, heading[2] ?? ''];
    const isRow = line.startsWith('|');
    if (isRow && !inTable) tables.push({ part, section, lines: [] });
    if (isRow) tables.at(-1)?.lines.push(line);
    inTable = isRow;
  }
  return tables.map(({ part, section, lines }) => {
    const [header, separator, ...rows] = lines.map(cellsOf);
    if (header === undefined || separator?.every((cell) => /^:?-+:?$/.test(cell)) !== true) {
      throw new Error(`markdown table under "${section || part}" without a header and a --- line`);
    }
    return {
      part,
      section,
      rows: rows.map((cells) => {
        if (cells.length !== header.length) throw new Error(`markdown row under "${section || part}" has ${cells.length} cells, the header ${header.length}: ${cells.join(' | ')}`);
        return Object.fromEntries(header.map((column, index) => [column, cells[index] ?? '']));
      }),
    };
  });
}

function cellsOf(line: string): string[] {
  return line
    .trim()
    .replace(/^\|/, '')
    .replace(/\|$/, '')
    .split('|')
    .map((cell) => cell.trim().replace(/^`(.*)`$/, '$1'));
}
