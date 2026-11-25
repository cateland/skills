---
name: code-comments
description: Delete, merge, or fix code comments until only earned ones remain. Use when writing or reviewing code comments, for the comment pass that ends a merge or pull request, or to record why a review suggestion was declined.
license: MIT
---

# Code Comments

An **earned** comment states a durable reason the code cannot show: why a non-obvious choice exists, an external constraint or business rule, a workaround and what removes it, a surprising invariant or edge case, or why the obvious alternative is wrong. Work **delete-first**: every comment in scope is a deletion candidate and stays only when earned.

## 1. Scope

- While writing code: the comments you write or touch.
- In the comment pass: every comment (leading, trailing, inline, doc comment) in each logical block the branch changes, per `git diff $(git merge-base origin/<default> HEAD)` plus uncommitted work, source and tests. Run it after the round's last code change. The pass edits comments only; list a rename or restructure it suggests in the report.

## 2. Verdict per comment (first that applies)

1. A clearer name, type, or structure says it: change the code (comment pass: suggest it), delete the comment.
2. Not earned: delete. This covers narration, a restated name/type/condition, review history, finding IDs, "intentionally", and in tests a restated test name, table row, or mock return.
3. Several comments govern one construct: compose them into one, at the smallest construct they govern.
4. Earned, but wrong, stale, or on the wrong construct: rewrite or move it. Earned and correct: keep it word for word, wrapping included.
5. Earned information is missing: add one comment.

A ticket key stays when it is the authority to consult (`PAY-12 rule 7`) or sits in a `HACK` / `TODO` marker's text. Tool directives, generated markers, and required API docs keep their exact form.

Words: the repository glossary (`CONTEXT.md` or `GLOSSARY.md`, or the file a `CONTEXT-MAP.md` / `GLOSSARY-MAP.md` picks), else the code's terms. ASD-STE100 Simplified Technical English, one sentence per idea.

## 3. Declined review suggestion

The code keeps the durable reason: one comment at the finding's lines that names the rule and says why it does not fit here, composed with any comment already on that construct. This comment is earned; later passes keep it. The decline itself (finding ID, "declined", review round) goes in the review thread reply.

## 4. Examples

Before: four lines on one statement, half of them history.

```ts
// Same module as <Document>/<Page>, per react-pdf. Bundled worker, no CDN.
// SSR is skipped by the caller's dynamic import of this module.
// pdfjs-dist pinned to the version react-pdf pins, so the package manager dedupes to one copy;
// a mismatch adds a second copy, not a silent break.
```

After: only what a reader cannot see.

```ts
// Set in the module that renders <Document>/<Page> (react-pdf requirement).
// No SSR guard: the caller loads this module with ssr: false.
```

Test comments that the code already shows: delete both.

```ts
// real i18next with flat keys, so the returned text is the resolved message
// mocked t returns its key, so the toast shows RULE_KEY
```

Declined review suggestion, composed with the comment already on the constant:

```ts
// One key for all rules: rule texts belong to the client rules configuration (PAY-12 rule 7).
// Error-key family, not features/pages/components: a shared translator must not depend on a page path.
```

## 5. Report (comment pass and review)

One line per comment in scope: `file:line → deleted | merged | rewritten | kept: <reason>`, then the counts. In a review task, report the same lines as findings and edit nothing.

**Complete when** every comment in scope has a verdict in the report and every kept comment is earned.
