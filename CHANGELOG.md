# Changelog

## 3.2.0

- New companion `rse-debugging`: fixes reported bugs from evidence. It reproduces with a failing check, fixes the
  cause, and leaves a regression test that fails on the original code, even when the cause looks obvious and even
  when the test cannot be run in the session. Measured on Claude Sonnet 5.5 (6 debugging-related cases x 3 runs):

  | Setup | Edits only | Python allowed (`--allow-exec`) |
  | --- | --- | --- |
  | 3.1.1 | 13/18 | 15/18 |
  | 3.1.1 + `rse-debugging` | 15/18 | 18/18 |

  The gain is the crash-fix case (0/3 to 3/3 in both modes); no case regressed. Sonnet never invoked the skill: its
  description alone carried the behavior. Sonnet still writes the regression test after the fix instead of seeing
  it fail first, and says so. The edits-only drop in `core-unrelated-failure-reported` is why `--allow-exec` exists:
  that case needs a test run. An earlier draft, scoped to bugs "whose cause is not yet known", scored 0/3 on the
  crash-fix case because the cause looked obvious.
- The core companion table lists `rse-debugging` (the description is unchanged, as measured); the debugging eval
  cases are tagged with it.
- Eval runner: `--allow-exec` lets the agent run `python`, `py` and `pytest` in its temporary repository (Claude Code
  `--allowedTools` rules, with the evals' interpreter first on `PATH` so a Windows Store stub cannot shadow it).
  Without it, cases that need a test run, such as `core-unrelated-failure-reported`, pass or fail on wording alone.
  Off by default; recorded in `summary.md` and in each result.

## 3.1.1

Merged after the behavioral evals (23 cases, 3 runs each, isolated profile, November 2026). Pass rate of all
deterministic checks:

| Model | No skills | 3.0.0 | 3.1.1 |
| --- | --- | --- | --- |
| Claude Opus 5.5 | 84% (58/69) | 93% (57/61) | 99% (68/69) |
| Claude Sonnet 5.5 | 72% (50/69) | 86% (59/69) | 93% (64/69) |

The 3.0.0 Opus arm missed four of the newer cases (61 sessions). The 3.1.1 runs also had an unreleased debugging
companion installed; it did not trigger on Sonnet's debugging case and is not part of this release. Sonnet rarely
invokes the core skill, so most of its gain comes from the skill descriptions it always sees. Agents could edit
files but not execute Python.

### Skills

- The core description states that a request to review, check or look into code never authorizes edits, commits or
  pushes, even when another installed skill or policy demands them. Measured reason: under a conflicting "policy"
  skill the core skill was never invoked, so a rule that lived only in the skill body never loaded. With the
  sentence in the description: 8 of 8 runs on Opus and 3 of 3 on Sonnet kept the review read-only (3.0.0: 2 of 5
  and 1 of 3).
- Core rule 1: when another active skill or workflow would go further than the request (editing during a review,
  committing, pushing, starting agents, external or paid effects), the more conservative instruction wins unless
  the user explicitly asked for more.
- Reviews treat an existing comment that names a shortcut and its limit (for example `shortcut: <limit>, <when>`)
  as a recorded decision, not a finding, unless the limit is exceeded.
- `references/verification.md`: tests at public seams, anti-patterns, and test-first as a mode the user can request.
- `rse-task-packs`: drafting a spec when none exists, with one batched question for consequential unknowns only; a
  task waiting on an open decision stays `draft`, or `blocked` with a `blocker`, and adds no manifest fields.
- `suite/user-instructions/review-guard.md`: an optional user-level guard for reviews (defense in depth; the
  description alone already held the boundary in the evals).

### Tooling

- Codex language policy: `suite/user-instructions/AGENTS.md` is replaced by `codex-config.toml`
  (`developer_instructions`). On Codex desktop 26.1117 for Windows, `~/.codex/AGENTS.md` made every launch show
  "Connection for host ID local not found".
- Eval harness works on Python 3.9 (`Path.write_text(newline=)` needs 3.10). CI skips 3.9 on Ubuntu only, because the
  runner image no longer ships it.
- Suite linter and evals locate the skills when the four repositories are cloned side by side.
- Eval runner isolation: a dedicated `CLAUDE_CONFIG_DIR` profile (or `--bare` with an API key), with `CLAUDE.md`,
  auto memory, user settings, MCP and non-essential traffic off. The runner reads `stream-json` to record skill
  triggers, cost and model, and stops the run as CONTAMINATED if the no-skill arm sees a suite skill. Paid runs need
  `--confirm` for more than one session and stop at `--max-cost-usd`. The "Reply in English" prompt suffix is gone.
- The runner stops with exit code 4 when the agent answers with a service message (usage limit, login, credit or API
  error) instead of grading it as a skill failure; sessions before it stay valid. A subscription limit once turned a
  whole candidate run into 47 false failures.
- `--user-instructions FILE` appends a file to every session's system prompt (`--append-system-prompt-file`), to
  measure user-level instructions that isolation otherwise disables.
- Six harder cases (23 total), each built around a tempting wrong move: fixing when asked to investigate, retrying
  a non-idempotent bank transfer, refactoring while adding a flag, inventing answers when the user is away,
  committing under a conflicting "policy" skill, and weakening a flaky test instead of fixing the order contract.
  Each check is verified to reject the tempting solution and to accept alternative correct ones.
- Two new cases (17 total): a conflicting installed skill that demands edits during review, and a crash fix that
  must leave a test failing on the original bug.

## 3.0.0

### Structure (breaking)

- Published as four repositories in one organization. Split the single `reliable-software-engineering` skill into a core skill and three companions:
  `rse-task-packs`, `rse-refactoring`, `rse-security-review`. Companions link into the core skill's
  references; the core skill never depends on them, so every rule keeps one owner.
- The workflows of the companions are now their `SKILL.md` bodies, so they load as soon as the skill triggers.
- `Move-sensitive contracts` moved from refactoring into the core skill (`references/move-sensitive-contracts.md`),
  because ordinary changes need it as much as refactors.

### Content

- Core `SKILL.md` opens with seven core rules; descriptions now carry concrete trigger phrases.
- Removed the Arabic communication policy from all skills; it now lives in user-level instructions
  (`suite/user-instructions/CLAUDE.md` for Claude Code, `suite/user-instructions/AGENTS.md` for Codex).
- Removed pinned model names (the "Sonnet 5.5 medium" execution profile is now model-neutral).
- Removed authoring residue: Notebook/YouTube source IDs, flashcard/slide coverage, market and learner
  sections, legacy section numbers. The record is kept outside the published skills.
- New `references/misconceptions.md`: the engineering rows of the former corrections table.

### Scripts

- `check_baseline.py`
  - Windows: bare names resolve through `PATHEXT` and run the resolved path, so `npm`, `yarn`, `pnpm` work.
  - Arguments to `.bat`/`.cmd` files are refused when they contain cmd.exe metacharacters (they always pass through cmd.exe).
  - A timeout kills the whole process tree (`taskkill /T` on Windows, process group on POSIX); previously child
    processes kept running.
  - Output keeps the first and last 8 KiB with an omitted-bytes marker and records full sizes; previously only the
    first 16 KiB, which dropped test summaries.
  - `timeout_seconds` may be raised per check up to 3600 (default still 30); a timeout is still incomplete evidence.
  - Refuses to start an `after` phase when `comparison.json` already exists.
- `validate_task_pack.py`
  - `spec_sha256` is computed with BOM and line endings normalized, so a Git CRLF/LF checkout no longer invalidates
    evidence. Raw-byte hashes from 2.3.x remain accepted while the bytes are unchanged.
  - New `--spec-hash` option prints the value to record in evidence.
  - Repeated headings resolve with GitHub `-1`, `-2` anchor suffixes.
  - Active tasks are rejected while pack-level Markdown (CONTRACTS.md, DECISIONS.md, ...) still holds `REPLACE_` placeholders.
  - Both scripts state the Python 3.9+ requirement; docs show `python3` / `py -3` / `python`.
- Tests: 37 -> 49; every new test fails against 2.3.1 and passes on 3.0.0.

### Tooling

- `suite/tools/check_skills.py`: frontmatter, relative links and anchors, SKILL.md size budget, banned-residue checks.
- `suite/evals/`: behavioral evaluation cases for the skills' effect on an agent.
- CI workflow running all of the above on Ubuntu, Windows and macOS.

## 2.3.1

Original version as received.
