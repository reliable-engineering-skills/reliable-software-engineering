# Changelog

## Unreleased

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
