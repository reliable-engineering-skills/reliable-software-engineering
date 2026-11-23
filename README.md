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
  - `suite/evals/`: 23 behavioral cases, a self-check (an idle agent fails, the reference passes) and an A/B
    runner that compares an agent with and without the skills.
  - `suite/user-instructions/`: an optional user-level language policy and an optional review guard (see below).
    The skills themselves are language-neutral.

## Optional: a user-level language policy

The skills never dictate a response language. To set one for yourself:

- **Claude Code:** copy `suite/user-instructions/CLAUDE.md` to `~/.claude/CLAUDE.md` and edit it.
- **Codex:** paste `suite/user-instructions/codex-config.toml` into `~/.codex/config.toml` (top level, before the first
  `[table]`). It sets `developer_instructions`.

> Avoid `~/.codex/AGENTS.md` for this on Codex desktop 26.1117 (Windows): with that file present, every launch showed
> "Uncaught Exception: Connection for host ID local not found". Removing it stopped the dialog, and
> `developer_instructions` applied the same policy without it.

## Optional: a user-level review guard

`suite/user-instructions/review-guard.md` states, as a user instruction, that a review or investigation request never
authorizes edits, commits or pushes, even when another installed skill demands them. Append it to `~/.claude/CLAUDE.md`
or to Codex `developer_instructions` if you install skills or plugins that push reviews toward changes. In our evals the
skill description alone already held this boundary on both models we measured, so the guard is defense in depth,
not a measured improvement.

## Behavioral evals

23 cases measure what the skills change in an agent's behavior. `check_evals.py` proves each case
discriminates (an idle agent fails, a reference solution passes) without calling any model.
`run_evals.py` runs a real agent with and without the skills; every session is a paid model call.

```powershell
py -3 suite/evals/check_evals.py                                    # validate the cases, offline
py -3 suite/evals/run_evals.py --check                              # isolation and plan, no model call
py -3 suite/evals/run_evals.py --cases core-review-is-read-only --confirm   # 2 sessions
py -3 suite/evals/run_evals.py --runs 5 --confirm --max-cost-usd 40         # full A/B
```

Isolation matters more than anything else: if the no-skill arm can see the skills (user-level installs,
`CLAUDE.md`, memory, settings, hooks, MCP), the comparison is meaningless.

- `--isolation profile` (default): a dedicated Claude Code profile through `CLAUDE_CONFIG_DIR`, with `CLAUDE.md`,
  auto memory, user settings, MCP servers and non-essential traffic off. Log in once inside that profile;
  `--check` prints the command.
- `--isolation bare`: `claude --bare` with skills passed through `--add-dir`. Needs `ANTHROPIC_API_KEY`.

By default the agent can edit files but every command that runs Python is denied, so cases measure decisions and
diffs. `--allow-exec` lets it run `python`, `py` and `pytest` inside the session's temporary repository, with the
interpreter that runs the evals first on `PATH`, so it can reproduce bugs and run tests. That is arbitrary code
running as your user: use it only with the suite's own fixtures, ideally in a disposable VM or container. Compare
runs only with the same setting; `summary.md` and every result record note it.

The runner reads each session's `stream-json` events. It records which skills were invoked (trigger rate),
the reported cost, and the model. If the no-skill arm invokes or lists a suite skill, the run stops as
CONTAMINATED instead of producing numbers. More than one session needs `--confirm`, and `--max-cost-usd`
(default 10) stops new sessions once the reported spend reaches it.

### Measured results

Each release lists its measured pass rates per model in the
[changelog](https://github.com/reliable-engineering-skills/reliable-software-engineering/blob/main/CHANGELOG.md).
Unless a release says otherwise, agents in those runs could edit files but not execute Python, so the cases
measure decisions and diffs, not test execution.

## License

MIT. Version 3.1.1; see the [core changelog](https://github.com/reliable-engineering-skills/reliable-software-engineering/blob/main/CHANGELOG.md).
