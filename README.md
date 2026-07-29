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

### `memory-diet`

Audits nested `AGENTS.md` and `CLAUDE.md` files so recurring context contains only guidance that is both undiscoverable and relevant throughout its scope.

The skill:

1. classifies every instruction as `KEEP`, `REMOVE`, `EXTRACT`, or `MOVE`
2. writes an evidence dossier for each proposed skill before changing memory
3. requests granular approval
4. applies only approved edits

Dossiers preserve source text, repository context, and Git provenance so skill extraction can happen in a later session. To turn a dossier into a skill, consider Matt Pocock's [`writing-great-skills`](https://github.com/mattpocock/skills); that repository's README contains its current installation instructions.

## Repository convention

Each skill lives under `skills/<skill-name>/`. Progressive-disclosure documents and templates attached to a skill live in its `agents/` directory.

## License

[MIT](LICENSE)
