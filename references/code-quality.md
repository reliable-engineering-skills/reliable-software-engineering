# Code quality and formatting for affected changes

Apply to the affected diff during implementation, or report findings in a review-only request. Reuse the project's formatter, linter, type checker, idioms, and supported language/version. Do not add a new style tool or reformat unrelated files without a task reason.

## Inspect and choose

- Read the owner, representative caller, neighboring conventions, and applicable instructions before editing. Trace indirect/framework/public use before deleting apparently unused code.
- Use names that explain domain meaning, units, and side effects where they matter. Generic short names are acceptable in a clear local context; avoid ambiguous helper/manager abstractions, not every variable named `result`.
- Keep functions cohesive and control flow understandable. Parameter objects, polymorphism, and extraction earn their cost when they clarify a real contract. Line counts, parameter counts, nesting, and complexity are investigation signals or project-configured checks, not universal limits.
- Use SOLID as a diagnostic lens: ownership (SRP), justified extension (OCP), substitutable contracts (LSP), consumer-focused interfaces (ISP), and dependency direction (DIP). A simple conditional or concrete class is not automatically a violation. Keep a small appropriate abstraction or none.
- DRY concerns repeated knowledge. Similar syntax with different business rules can stay separate. KISS favors understandable sufficient behavior. YAGNI removes speculative variants, while required validation, recovery, and authorized rollout controls remain necessary.

## Prevent common generated-code failures

Verify every new package, symbol, option, and provider call against installed source/official versioned documentation. A plausible name is not evidence an API exists. Consider standard-library/project capabilities first without reimplementing cryptography, parsers, or complex lifecycle behavior merely to avoid dependencies.

Do not replace required operations with hard-coded success, fixture values, broad exception suppression, disabled checks, or misleading fallback. Catch at an owner that can recover, translate safely, or perform required cleanup; top-level error boundaries may legitimately catch broadly while reporting failure. Preserve data-loss prevention and trust-boundary checks.

Check applicable empty/one/many, range, time, money, encoding, ownership, and async failure boundaries. Derive expected behavior from requirements rather than copying a nearby function's assumptions. Remove new dead imports/branches with evidence; keep public/dynamic exports and compatibility behavior until confirmed unused or removal is authorized.

## Comments, documentation, and formatting

Use comments/docstrings for contracts, rationale, constraints, units, safety, legally required attribution, or genuinely unclear behavior. Remove misleading/stale narration and abandoned code where safe. Do not ban useful explanations or require comments for every boundary case. Match the configured formatter/import order; avoid churn and manual formatting wars. Update existing affected documentation to reflect verified behavior without creating a new guide for every edit.

After a meaningful change, review the diff for scope, behavior, error paths, data exposure, hidden costs, actual dependencies, and test meaning. Run the relevant existing checks once; repeat only after an affected change, failure, or unresolved concern. Report only observed findings/fixes. Do not claim an independent reviewer ran when the same agent performed a self-review.

Sources: [Google Engineering Practices](standards-sources.md#s39), official language/project tooling, and the original authors' refactoring/design literature. Universal function-length, argument-count or complexity ceilings and blanket comment bans are deliberately not imposed.
