---
name: code-comments
description: Keep inline code comments useful, current, and sparse. Use when writing, editing, refactoring, or reviewing code, including when nearby comments can be added, merged, rewritten, or removed.
license: MIT
---

# Code Comments

An **earned comment** prevents a plausible future mistake by explaining information that the code cannot express. Default to no comment.

## 1. Use the project language

Read the applicable `CONTEXT.md` before you write or rewrite a comment. When the repository has more than one `CONTEXT.md`, use `CONTEXT-MAP.md` to select the applicable file. Use its ubiquitous language exactly and consistently. When no context file applies, use the terms in the code.

Write comments in ASD-STE100 Simplified Technical English. Use short, direct sentences, active voice, one topic per sentence, and one term for one meaning. Avoid idioms and ambiguous pronouns.

## 2. Inspect the comment neighborhood

Read the complete logical block around changed code, including its leading, trailing, and inline comments. Identify the code that each comment governs.

Use this action order:

1. Improve names, types, functions, control flow, or abstractions when clearer code can remove the comment.
2. Delete an unearned comment.
3. Compose consecutive comments that govern the same code into one coherent comment.
4. Rewrite an earned comment when its meaning, terminology, scope, or wording is no longer exact.
5. Add a comment only when earned information is still missing.

Place each surviving comment next to the smallest construct that it governs. Keep separate comments only when they govern different constructs.

## 3. Test whether a comment is earned

Keep or write a comment when it explains:

- why a non-obvious choice exists
- an external constraint or business rule
- a workaround and why it is necessary
- a surprising invariant, side effect, or edge case
- why an obvious alternative is wrong

Delete or rewrite a comment that:

- describes the code or language syntax
- restates a name, type, condition, or signature
- walks through the implementation
- records history, a task, a prompt, an issue, or a conversation
- defends an ordinary choice with words such as “intentionally” or “deliberately”
- is stale, speculative, or attached to the wrong scope

Describe why the code is this way now. Prefer durable constraints to implementation details that can change during a refactor.

Treat tool directives, generated markers, and required API documentation as contracts. Preserve their required form and follow the repository convention.

## 4. Audit the result

For each modified logical block, inspect every comment again. Each comment must:

1. contain information that the code cannot express
2. explain a reason, constraint, or non-obvious context
3. reduce the chance of a plausible future mistake
4. use the applicable ubiquitous language
5. be current, durable, and attached to one clear target
6. be composed with adjacent comments that govern the same target

Delete any comment that fails this audit. In a review task, report the same defect and the required action instead of editing it.

**Complete when:** every comment in each modified logical block is earned, exact, and sparse.
