# Contributing

## Change sequence

1. Identify the semantic owner in `specification/`.
2. Change normative semantics first.
3. Change exact representations in `contracts/`.
4. Update reference interfaces, lifecycle tables, examples, and migration notes.
5. Add or strengthen a deterministic drift check.
6. Preserve moved public URLs in `docs.json`.
7. Run the complete validation suite.

## Design test

Before adding a core concept, ask whether it needs independent identity, lifecycle, concurrency control, policy, retention, or audit across materially different domains. If not, keep it as a field, event, artifact subtype, projection, or optional extension.

## Compatibility

Published resource versions and contract versions are immutable. Breaking serialized changes require a new semantic version and migration guidance. A Run never changes execution-authority profile in place.
