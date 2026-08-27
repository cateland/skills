# Agent Skills

A public collection of harness-neutral skills for coding agents. Skills follow the [Agent Skills standard](https://agentskills.io/specification) and are intended to work across Pi, Claude Code, Codex, Gemini CLI, and other compatible agents.

## Install

Use the [`skills` CLI](https://github.com/vercel-labs/skills) to choose a skill and target agent interactively:

```bash
npx skills add cateland/skills
```

To select `memory-diet` directly:

```bash
npx skills add cateland/skills --skill memory-diet
```

The CLI also supports `--agent pi`, `--agent claude-code`, `--agent codex`, and `--agent gemini-cli`.

## Skills

### `code-comments`

Keeps comments useful and sparse while code is written, edited, refactored, or reviewed. It uses the repository's ubiquitous language and ASD-STE100 Simplified Technical English, and it treats nearby comments as one composition that can be kept, merged, rewritten, or removed.

### `memory-diet`

Audits nested `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` files so recurring context contains only guidance that is relevant throughout its scope or supplies a required activation path.

The skill:

1. classifies every instruction as `KEEP`, `REMOVE`, `EXTRACT`, or `MOVE`
2. distinguishes searchable information from guidance reached through a concrete pre-decision activation path
3. writes an evidence dossier for each proposed skill and blocks removal until an active replacement exists
4. requests granular approval
5. applies only approved, eligible edits

Dossiers preserve source text, repository context, and Git provenance so skill extraction can happen in a later session. To turn a dossier into a skill, consider Matt Pocock's [`writing-great-skills`](https://github.com/mattpocock/skills); that repository's README contains its current installation instructions.

## Repository convention

Each skill lives under `skills/<skill-name>/`. Progressive-disclosure documents and templates attached to a skill live in its `agents/` directory.

## License

[MIT](LICENSE)
