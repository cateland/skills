---
name: memory-diet
description: Diet repository AGENTS.md, CLAUDE.md, and GEMINI.md through an activation-aware audit that preserves conditional guidance as skill-plan dossiers. Use when the user explicitly starts this process or asks to extract skill candidates from those files; routine instruction edits are outside its scope.
license: MIT
---

# Memory Diet

A **diet** keeps recurring memory only when it earns its context cost. An **activation path**, rather than file visibility, makes replacement guidance discoverable. Conditional guidance leaves memory as a skill-plan **dossier**: evidence for a later skill-writing session, not a premature skill design.

## 1. Discover the effective memory

Find every repository-owned file named exactly `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`, including nested files. Ignore personal/local variants unless the user includes them. Record:

- each file's directory scope
- the starting Git revision and working-tree state, when available
- which instructions are inherited into each scope

When several file types govern a scope, treat `AGENTS.md` as the tool-neutral home and `CLAUDE.md` and `GEMINI.md` as homes for harness-specific bridges or guidance. When only a harness-specific file exists, preserve the established convention and suggest `AGENTS.md` in the report rather than creating it.

**Complete when:** every in-scope `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` and its effective scope are accounted for.

## 2. Classify every instruction

Give every substantive instruction exactly one verdict. Track removal readiness separately: `ELIGIBLE` or `BLOCKED`.

| Verdict | Test |
|---|---|
| `KEEP` | Applies throughout the scope and is undiscoverable or supplies a required activation path |
| `REMOVE` | Stale, contradicted, duplicated by effective memory, or recovered through a concrete pre-decision activation path |
| `EXTRACT` | Useful conditional or domain-specific steering that belongs in an on-demand skill |
| `MOVE` | Retained guidance belongs in another existing scoped or tool-neutral memory file |

### Require an activation path

Treat replacement information as discoverable only when an ordinary relevant task reaches its source before the affected decision. Use this counterfactual:

> If this memory instruction disappeared, what ordinary task step would cause the agent to read the replacement source before deciding?

A qualifying activation path names both the trigger and the source, such as:

- a harness-loaded or imported instruction file
- source or configuration followed while performing the relevant task
- an enforced script, test, or hook
- an installed, in-scope skill validated against representative triggers

A descriptive path, root listing, broad search, or repository-wide availability establishes retrievability, not activation. Human workflow choices, preferred tools, exact labels, safety boundaries, and requirements to consult another document need explicit routing.

A memory pointer is routing guidance. `KEEP` it when it applies throughout the scope and is the sole activation path. `EXTRACT` it when conditional. Mark its removal `ELIGIBLE` only when an active replacement reliably loads the target; otherwise mark removal `BLOCKED` and retain the pointer. A dossier records evidence for a future replacement and provides no runtime activation.

Use this decision order:

1. Is it stale, contradicted, or already inherited from effective memory? `REMOVE`.
2. Does a concrete activation path survive deletion and recover the instruction before the affected decision? `REMOVE`.
3. Does it belong in another existing memory file where it would be relevant throughout that target scope? `MOVE`.
4. Does it apply to every task under its current directory scope? If not, `EXTRACT` and record removal readiness.
5. Otherwise, `KEEP`.

If instructions conflict, show both scopes and provenance and mark the resolution as blocked. Let the user choose the winner.

**Complete when:** every substantive instruction has exactly one verdict; every `REMOVE` cites pre-decision activation or stale, contradictory, or duplicate evidence; every `EXTRACT` has removal readiness; and every conflict is explicit.

## 3. Write dossiers before changing memory

Group related `EXTRACT` items by proposed skill, even when they came from several files. Resolve the dossier directory in this order:

1. a planning directory documented by the repository
2. an established `.agents/skill-plans/` or `.claude/skill-plans/` convention
3. `.agents/skill-plans/`

Read [`agents/SKILL-PLAN.template.md`](agents/SKILL-PLAN.template.md), then write one `<skill-name>.md` dossier per candidate. Preserve exact source excerpts and their provenance. Inspect relevant Git history for intent when available; record unavailable or uncommitted evidence honestly.

A dossier supplies evidence to a skill writer. It does not decide frontmatter, invocation, leading words, branches, steps, completion criteria, or progressive disclosure for the future skill. It also does not activate its source guidance.

For every candidate, record the target reference, proposed replacement mechanism, activation trigger, activation evidence, and removal readiness. When readiness is `BLOCKED`, set the planned source edit to retain pending an active replacement.

**Complete when:** every `EXTRACT` row names a written dossier, every excerpt is represented exactly once, and each dossier records provenance, activation evidence, and `ELIGIBLE` or `BLOCKED` removal readiness.

## 4. Report and request granular approval

Report per memory file:

- its scope and measured current line and character counts
- the exhaustive classification table with evidence
- dossiers written during analysis
- conflicts and suggested convention changes
- blocked removals and the active replacements they still need
- any file that would become empty, with its deletion listed as a separate approval item

Offer only a light observation prompt: after applying the diet, the user may compare available initial-context usage and representative task quality, watching for missed instructions, irrelevant output, or extra exploration. State no unmeasured token, productivity, or quality claims.

For later extraction, suggest installing and using `writing-great-skills` from [Matt Pocock's skills repository](https://github.com/mattpocock/skills), whose README contains current installation instructions.

Request item-level approval for eligible memory edits and file deletions. Present blocked removals as follow-up work rather than approval items. End the turn with every `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` byte-for-byte unchanged; the newly written dossiers are the only analysis-phase file changes.

**Complete when:** the user can approve or reject each eligible edit and deletion, every blocked removal names its missing replacement, and the memory files remain unchanged.

## 5. Apply only approved edits

Apply approved `REMOVE` and `MOVE` rows. Apply an approved `EXTRACT` removal only when its readiness is `ELIGIBLE`, while preserving rejected, unresolved, and blocked instructions exactly. Move guidance only into an existing target memory convention; when the tool-neutral target does not exist, leave the instruction in place and retain the suggestion in the report.

After editing:

- verify every changed instruction against its approved verdict
- verify each removed `EXTRACT` instruction is loaded by its active replacement for representative relevant tasks; the dossier remains evidence only
- remove an empty memory file only when its deletion was explicitly approved and repository tooling does not require it
- report measured resulting line and character counts alongside the resulting diff
- leave the working tree for the user to commit

**Complete when:** every memory edit and deletion maps to an approved, eligible item; every rejected, unresolved, or blocked item is untouched; and the final diff contains no unsolicited commit.
