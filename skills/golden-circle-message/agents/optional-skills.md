# Optional skills

Use an already available skill first. When one is missing, offer its installation command or offer to install it for the user. If the user declines, use the conversational fallback for `grilling` or revise the prose directly without `stop-slop`.

## Sources and commands

- **`grilling` — Matt Pocock:** [source](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling).

  ```bash
  npx skills@latest add mattpocock/skills --skill grilling
  ```

- **`stop-slop` — Hardik Pandya:** [one published implementation](https://github.com/hardikpandya/stop-slop).

  ```bash
  npx skills@latest add hardikpandya/stop-slop --skill stop-slop
  ```

The user can run either command and choose the target agent and installation scope interactively.

## Agent-run setup

1. Inspect the selected source's `SKILL.md` and referenced instructions before proposing installation. For an unfamiliar implementation, confirm that it is the one the user wants.
2. Get approval for the source, target agent, and project-local or global scope. A drafting request alone is not installation approval.
3. Run the matching command with `--agent <agent-id> --yes`; add `--global` only for approved global installation. If execution or network access is unavailable, give the user the command instead.
4. Verify that the skill was installed for the selected agent and read its instructions before using it. If discovery requires a session reload, tell the user and use the fallback for the current draft.
