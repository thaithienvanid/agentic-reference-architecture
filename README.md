# Agentic Reference Architecture

A framework-agnostic, evaluation-driven specification and executable contract set for production AI agents, deterministic and agentic workflows, durable execution, multi-agent systems, enterprise platforms, multi-tenant SaaS, and governed marketplaces.

> **Models propose. Deterministic software, policy, resource authorization, and humans authorize. The runtime executes, persists, and records.**

ARA 1.0 is an independent candidate technical specification. It is not an RFC Series publication, formal standards-body standard, legal certification, security attestation, or proof of operational effectiveness.

## Start here

- [`guides/adoption.mdx`](./guides/adoption.mdx) — select Core plus only the modules you need and build one vertical slice.
- [`specification/index.mdx`](./specification/index.mdx) — normative scope, composable modules, invariants, and reading order.
- [`specification/boundaries-and-use-cases.mdx`](./specification/boundaries-and-use-cases.mdx) — domain, application, kernel, runtime, port, and adapter boundaries.
- [`cheatsheets/architecture.mdx`](./cheatsheets/architecture.mdx) — canonical vocabulary and decision rules.
- [`reference/contract-catalog.mdx`](./reference/contract-catalog.mdx) — schemas, registries, fixtures, API/event profiles, and validation.
- [`handbook/runtime.mdx`](./handbook/runtime.mdx) — build the atomic durable runtime.
- [`handbook/ports-and-adapters.mdx`](./handbook/ports-and-adapters.mdx) — implement and verify a provider or protocol adapter.
- [`examples/index.mdx`](./examples/index.mdx) — software delivery, customer service, incident response, procure-to-pay, and synthetic research.
- [`reference/conformance-checklist.mdx`](./reference/conformance-checklist.mdx) — assess selected modules and profiles against reproducible evidence.

## Normative reading order

1. [`specification/boundaries-and-use-cases.mdx`](./specification/boundaries-and-use-cases.mdx)
2. [`specification/resource-model.mdx`](./specification/resource-model.mdx)
3. [`specification/execution-model.mdx`](./specification/execution-model.mdx)
4. [`specification/runtime.mdx`](./specification/runtime.mdx)
5. [`specification/data-and-evidence.mdx`](./specification/data-and-evidence.mdx)
6. [`specification/platform.mdx`](./specification/platform.mdx)
7. [`specification/security-and-governance.mdx`](./specification/security-and-governance.mdx)
8. [`specification/evaluation-and-conformance.mdx`](./specification/evaluation-and-conformance.mdx)
9. [`reference/conventions.mdx`](./reference/conventions.mdx)
10. [`reference/interfaces.mdx`](./reference/interfaces.mdx)
11. [`reference/lifecycles.mdx`](./reference/lifecycles.mdx)
12. [`reference/events-and-state.mdx`](./reference/events-and-state.mdx)
13. [`reference/contract-catalog.mdx`](./reference/contract-catalog.mdx)

## Canonical vocabulary

```text
Agent -> AgentVersion -> AgentRun
Workflow -> WorkflowVersion -> WorkflowRun
ExecutionPlan -> ExecutionPlanVersion -> ExecutionPlanRun

AgentRun
└── exactly one root WorkflowRun

WorkflowRun
└── ActivityRun
    ├── ActivityAttempt
    ├── ExecutionBranch
    ├── Iteration
    └── Effect
        └── Invocation

WorkerLease
ExperimentRun -> ExperimentVariant -> ExperimentTrial -> ExecutionSubjectRef
```

`Run` is reserved for independently addressable durable execution. The core does not define unqualified `Step`, `Round`, `AttemptRun`, `TrialRun`, `SubAgent`, or `SubWorkflow`.

## Composable conformance modules

```text
ARA Core

Optional:
  ARA Durable
  ARA Multi-Tenant
  ARA Enterprise Operations
  ARA Marketplace
  ARA High-Assurance
  ARA Regulated
```

`ARA Enterprise` is a convenience bundle for Core + Durable + Enterprise Operations, plus Multi-Tenant when shared tenants exist.

## Machine-readable contracts

```text
contracts/
├── schemas/      JSON Schema Draft 2020-12
├── registries/   effect, event, error, hard-gate and module IDs
├── examples/     executable fixtures
├── openapi/      optional HTTP API profile
└── asyncapi/     optional event-delivery profile
```

The specification owns semantics. A named machine contract owns serialized shape for its version/profile. A mismatch is handled as an erratum, not silently reconciled by implementations.

## Documentation site and validation

Markdown/MDX is the source of truth; Mintlify renders the site. Navigation and redirects live in [`docs.json`](./docs.json).

```bash
python -m pip install --requirement requirements-docs.txt
python scripts/check_contracts.py
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
npm install --global mint@4.2.687
mint validate
mint broken-links
```

## Repository map

```text
specification/  normative semantic specification and conformance modules
contracts/      exact machine-readable representations and fixtures
reference/      terminology, interfaces, lifecycles, profiles, checklist, diagrams
guides/         adoption and reader pathways
handbook/       application, runtime, integration, security, and operations guides
evaluation/     evaluation-driven development and adapters
implementation/ module layout, rollout, testing, and resilience
patterns/       reusable compositions
examples/       complete enterprise worked examples
decisions/      decision guide and ADRs
research/       primary evidence, use cases, findings, and comparisons
project/        documentation, release, and review governance
```

The [documentation architecture](./project/documentation-architecture.mdx) defines authority, page contracts, reader journeys, canonical ownership, quality, lifecycle, redirects, and change propagation. [Release and errata governance](./project/releases-and-errata.mdx) defines Candidate/Stable status, versioning, compatibility, validation, independent review, and corrections.

## Contributing

A semantic or contract change is incomplete until specification, machine contracts, reference material, conformance evidence, guides, examples, diagrams, ADRs, release notes, and automated checks agree. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`AGENTS.md`](./AGENTS.md).
