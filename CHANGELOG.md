# Changelog

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
