---
name: memory-diet
description: Diet AGENTS.md and CLAUDE.md through a deliberate audit that deduplicates recurring instructions and preserves conditional guidance as skill-plan dossiers. Use when the user explicitly starts this process or asks to extract skill candidates from those files; routine instruction edits are outside its scope.
license: MIT
---

# Memory Diet

A **diet** keeps recurring memory only when it earns its context cost. Conditional guidance leaves memory as a skill-plan **dossier**: evidence for a later skill-writing session, not a premature skill design.

## 1. Discover the effective memory

Find every repository-owned file named exactly `AGENTS.md` or `CLAUDE.md`, including nested files. Ignore personal/local variants unless the user includes them. Record:

- each file's directory scope
- the starting Git revision and working-tree state, when available
- which instructions are inherited into each scope

When both file types govern a scope, treat `AGENTS.md` as the tool-neutral home and `CLAUDE.md` as the home for Claude-specific guidance. When only `CLAUDE.md` exists, preserve the established convention and suggest `AGENTS.md` in the report rather than creating it.

**Complete when:** every in-scope memory file and its effective scope are accounted for.

## 2. Classify every instruction

Give every substantive instruction exactly one verdict:

| Verdict | Test |
|---|---|
| `KEEP` | Undiscoverable through reasonable repository exploration and relevant to every task in this directory scope |
| `REMOVE` | Discoverable, stale, contradicted, or duplicated by effective memory |
| `EXTRACT` | Useful conditional or domain-specific steering that belongs in an on-demand skill |
| `MOVE` | Retained guidance belongs in another existing scoped or tool-neutral memory file |

Use this decision order:

1. Can current source, configuration, scripts, imports, or repository structure recover it reliably? `REMOVE`.
2. Is it stale, contradicted, or already inherited from another memory file? `REMOVE`.
3. Does it belong in another existing memory file where it would be relevant throughout that target scope? `MOVE`.
4. Does it apply to every task under its current directory scope? If not, `EXTRACT`.
5. Otherwise, `KEEP`.

Human intent, safety boundaries, non-obvious environment constraints, and preferences between multiple valid tools are not discoverable merely because related code exists.

If instructions conflict, show both scopes and provenance and mark the resolution as blocked. Let the user choose the winner.

**Complete when:** the classification accounts for every substantive instruction exactly once, and every conflict is explicit.

## 3. Write dossiers before changing memory

Group related `EXTRACT` items by proposed skill, even when they came from several files. Resolve the dossier directory in this order:

1. a planning directory documented by the repository
2. an established `.agents/skill-plans/` or `.claude/skill-plans/` convention
3. `.agents/skill-plans/`

Read [`agents/SKILL-PLAN.template.md`](agents/SKILL-PLAN.template.md), then write one `<skill-name>.md` dossier per candidate. Preserve exact source excerpts and their provenance. Inspect relevant Git history for intent when available; record unavailable or uncommitted evidence honestly.

A dossier supplies evidence to a skill writer. It does not decide frontmatter, invocation, leading words, branches, steps, completion criteria, or progressive disclosure for the future skill.

**Complete when:** every `EXTRACT` row names a written dossier, every excerpt is represented exactly once, and each dossier records a revision or an explicit uncommitted/no-history state.

## 4. Report and request granular approval

Report per memory file:

- its scope and measured current line and character counts
- the exhaustive classification table with evidence
- dossiers written during analysis
- conflicts and suggested convention changes
- any file that would become empty, with its deletion listed as a separate approval item

Offer only a light observation prompt: after applying the diet, the user may compare available initial-context usage and representative task quality, watching for missed instructions, irrelevant output, or extra exploration. State no unmeasured token, productivity, or quality claims.

For later extraction, suggest installing and using `writing-great-skills` from [Matt Pocock's skills repository](https://github.com/mattpocock/skills), whose README contains current installation instructions.

Request item-level approval for the proposed memory edits and file deletions. End the turn with every `AGENTS.md` and `CLAUDE.md` byte-for-byte unchanged; the newly written dossiers are the only analysis-phase file changes.

**Complete when:** the user can approve or reject each proposed edit and deletion, and the memory files remain unchanged.

## 5. Apply only approved edits

Apply approved rows while preserving rejected and unresolved instructions exactly. Move guidance only into an existing target memory convention; when the tool-neutral target does not exist, leave the instruction in place and retain the suggestion in the report.

After editing:

- verify every changed instruction against its approved verdict
- verify each extracted instruction remains recoverable from its dossier
- remove an empty memory file only when its deletion was explicitly approved and repository tooling does not require it
- report measured resulting line and character counts alongside the resulting diff
- leave the working tree for the user to commit

**Complete when:** every memory edit and deletion maps to an approved item, every rejected or blocked item is untouched, and the final diff contains no unsolicited commit.
