# ARA machine-readable contracts

This directory contains the exact representation contracts for the Agentic Reference Architecture candidate specification.

Authority:

```text
specification/   semantic meaning
contracts/       exact representation for declared profiles
reference/       lookup and explanatory views
```

## Layout

```text
schemas/         JSON Schema Draft 2020-12 contracts
registries/      versioned identifiers and applicability metadata
examples/        fixtures validated against matching schemas
openapi/         HTTP API reference profile
asyncapi/        event-delivery reference profile
```

## Versioning

- Contract files declare stable `$id` values and `contractVersion` fields.
- Patch releases correct defects without intentionally changing meaning.
- Minor releases add compatible optional behavior.
- Major releases may break representation compatibility and require migration guidance.
- Published schemas, registries, and examples are immutable within a release.

## Validation

```bash
python scripts/check_contracts.py
```

The validator checks JSON Schema meta-schema validity, fixture conformance, registry structure and uniqueness, and OpenAPI/AsyncAPI/YAML structure. Documentation CI runs it together with the documentation consistency and Mintlify checks.