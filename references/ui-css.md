# UI and CSS engineering

Use when creating or changing a web interface, shared component, theme, or stylesheet. For an existing small edit inspect only the affected styles, component, and representative consumers. A design review produces findings; implement only when implementation is requested. Match the existing product languages and visual direction.

## Inspect before styling

Find the actual global stylesheet, theme configuration, tokens, shared components, and styling conventions. Do not assume Tailwind, a particular CSS filename, or a component library exists. Trace the cascade and component variants responsible for the affected result; appending an override can conceal the actual owner.

Identify the page's primary action, content hierarchy, supported languages/directions, representative viewport/input modes, and relevant state transitions. Reuse the existing shell and components rather than creating a second layout for a feature or development stage.

## Build with a single visual system

1. Reuse equivalent typography, color, spacing, size, radius, elevation, focus, motion, and layer tokens. Use semantic meaning where the project supports it; do not add a nearly identical one-off value beside an existing token.
2. When a reusable value is genuinely missing, extend the established token mechanism. A thin project may need a small coherent set, not a parallel theme framework. A local exception can remain local with a clear reason.
3. Put repeated visual behavior in an existing component/variant or a justified shared pattern. Prefer a clear layout over arbitrary positioning and cascading patches. Flexbox, Grid, local spacing, and fixed dimensions can each be appropriate for their actual purpose.
4. Style the relevant hover, focus-visible, active, disabled, validation, loading, empty, error, and success states. Preserve contrast and interaction clarity across the supported themes; a new theme is a separate product choice.
5. When a shared token or component changes, inspect representative consumers, including dense, long-text, and error uses. Do not redesign unrelated pages to enforce a new preference.

Use descriptive ownership and the project's selectors/scoping approach. Investigate clipping, positioning, and stacking contexts before changing z-index. Avoid broad specificity escalation or hiding page overflow to conceal a layout defect.

## Responsive and accessible behavior

Choose content-driven breakpoints compatible with the existing scale. Check intermediate widths, long/translatable text, page/text zoom, and portrait/landscape where relevant. Two-dimensional content such as a table may need local scrolling or an alternative; fixed/sticky controls must not cover the active input when a virtual keyboard opens. Use logical spacing/direction-aware layout when the supported locales require RTL/LTR.

Support the actual touch, pointer, and keyboard interactions. Provide visible focus, meaningful labels, semantic controls, comprehensible validation/error feedback, and alternatives to hover-only or gesture-only actions. Preserve supported themes and reduced-motion behavior. For new web UI without a stated target, use WCAG 2.2 AA as a proposed engineering target, recording scope and unverified areas; never present this default or an automated score as conformance or legal certification.

Inspect the stated browser/platform support and use the framework's existing mechanisms and appropriate fallbacks. A screenshot at one width does not prove usability on all devices; distinguish emulation from a real-device check.

## Independent sections and loading

Essential content should not wait for an unrelated optional panel. Start genuinely independent reads safely, give each usable section scoped loading/empty/error/retry behavior, and preserve shared layout with appropriately sized placeholders. Keep keyboard focus and status announcements stable; avoid a page-wide spinner when most of the page is usable.

A coherent result or shared authorization may require a grouped wait. Do not split such a dependency merely for animation. Ignore obsolete read results after navigation or input changes where safe, and retry one failed section without refetching everything. Client cancellation does not roll back a submitted server mutation. See [async and cache](async-cache.md) for scheduling and stale-data controls.

## Evidence to obtain

Use the changed journey and representative states. Check keyboard/focus, field errors, reflow/zoom, clipping, supported directions/themes, and relevant browsers. If a shared design primitive changed, inspect representative consumers. Combine applicable automated accessibility checks with manual interaction checks; report missing coverage honestly.

For a progressive-loading change, deliberately delay/fail an optional section and verify essential content is usable and its retry is scoped. Check that obsolete results cannot overwrite newer state. For a performance claim compare the actual journey and comparable device/network conditions; more concurrent requests alone is not evidence of improvement.
