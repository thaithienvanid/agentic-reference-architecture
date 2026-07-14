# ARA machine-readable contracts

This directory contains the exact representation contracts for the Agentic Reference Architecture 1.0 candidate specification.

```text
specification/   semantic meaning and invariants
contracts/       exact serialized representation for declared versions/profiles
reference/       lookup, profile, and explanatory views
```

A contract cannot silently redefine specification semantics. A semantic/representation mismatch is an erratum.

## Layout

```text
schemas/         JSON Schema Draft 2020-12 contracts
registries/      versioned identifiers and applicability metadata
examples/        executable fixtures matching schemas
openapi/         optional OpenAPI 3.1.1 HTTP profile
asyncapi/        optional AsyncAPI 3.0.0 event-delivery profile
```

The contract set covers run state, activity results, effects, invocations, events, atomic transition commits, worker leases, child-run links, capability grants, approvals, deployment snapshots, experiment trials, evaluation results, hard-gate registries, package locks, and package installation revisions.

## Rules

- Every schema declares a stable `$id` and explicit `contractVersion`.
- Every non-common schema has a matching `*.example.json` fixture.
- SHA-256 content digests use `sha256:` plus exactly 64 hexadecimal characters.
- Undeclared fields are rejected unless a namespaced extension point is intentional.
- Registry IDs are unique and immutable within a registry version.
- Production deployments and activated package installations contain exact versions and digests; source package releases may declare constraints that resolve into a `PackageLock`.
- Secrets, authorization headers, and private hidden reasoning are prohibited.

## Validation

```bash
python -m pip install --requirement requirements-docs.txt
python scripts/check_contracts.py
```

The validator checks JSON Schema meta-validity, fixture conformance, references, canonical digests, registry structure and uniqueness, hard-gate consistency, OpenAPI/AsyncAPI structure, and JSON/YAML code fences in the documentation.

Documentation CI runs contract validation together with documentation consistency, `docs.json`, Mintlify, and internal-link validation. A passing contract check proves representation consistency; it does not by itself prove implementation conformance, security, or operational effectiveness.
