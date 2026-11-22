# reliable-software-engineering

Proportionate, evidence-based engineering decisions: scope, smallest sufficient change, contracts, payments and data history, authorization, caching, operations and honest verification.

Part of the **RSE skill suite**: four complementary agent skills for Claude Code and Codex. One core skill
holds the shared rules; each companion adds one workflow and points back to the core, so every rule has
exactly one owner.

| Skill | Role | What it does |
| --- | --- | --- |
| **reliable-software-engineering** (this repo) | Core (required) | Proportionate, evidence-based engineering decisions: scope, smallest sufficient change, contracts, payments and data history, authorization, caching, operations and honest verification. |
| [rse-task-packs](https://github.com/reliable-engineering-skills/rse-task-packs) | Companion | Turns accepted work into portable, resumable task packs for another agent or a later session, with a structural validator. |
| [rse-refactoring](https://github.com/reliable-engineering-skills/rse-refactoring) | Companion | Behavior-preserving refactoring and codebase rescue, one responsibility at a time, with a before/after check recorder. |
| [rse-security-review](https://github.com/reliable-engineering-skills/rse-security-review) | Companion | Focused security review: trace untrusted input to sensitive sinks and report evidence-graded findings without touching production. |

## Install the suite

The companions link into the core skill's files, so install all four side by side.

Claude Code (PowerShell):

```powershell
foreach ($r in "reliable-software-engineering", "rse-task-packs", "rse-refactoring", "rse-security-review") { git clone "https://github.com/reliable-engineering-skills/$r" "$env:USERPROFILE\.claude\skills\$r" }
```

Claude Code (bash/zsh):

```bash
for r in reliable-software-engineering rse-task-packs rse-refactoring rse-security-review; do git clone "https://github.com/reliable-engineering-skills/$r" ~/.claude/skills/$r; done
```

Codex: clone the same four repositories into `~/.codex/skills/`. Update later with `git pull` in each folder.

## Contents

- `SKILL.md`: seven core rules, then scope, solution choice and proportionate verification.
- `references/`: loaded on demand (architecture, code quality, verification, API contracts, data and payments,
  security and controls, async and cache, UI/CSS, operations, systems lifecycle, misconceptions, sources).
- `suite/`: development tooling for the whole suite, not loaded by agents:
  - `suite/tools/check_skills.py`: lints all four skills (frontmatter, links, anchors, residue).
  - `suite/evals/`: 15 behavioral cases, a self-check (an idle agent fails, the reference passes) and an A/B
    runner that compares an agent with and without the skills.
  - `suite/user-instructions/`: an optional user-level language policy for `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`.
    The skills themselves are language-neutral.

## Behavioral evals

```powershell
py -3 suite/evals/check_evals.py                                   # validate the cases, offline
py -3 suite/evals/run_evals.py --agent claude --runs 1 --cases core-review-is-read-only   # calls a paid model
```

The runner needs the `claude` CLI (or `--agent codex`, whose flags you should confirm for your version).

## License

MIT. Version 3.0.0; see the [core changelog](https://github.com/reliable-engineering-skills/reliable-software-engineering/blob/main/CHANGELOG.md).
