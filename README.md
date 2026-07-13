# Agentic Reference Architecture

A framework-agnostic, evaluation-driven specification for production AI agents, deterministic and agentic workflows, durable execution, multi-agent systems, enterprise platforms, and governed marketplaces.

> **Models propose. Deterministic software, policy, and humans authorize. The runtime executes, persists, and records.**

ARA is an independent technical specification. It is not an RFC Series publication, a formal standards-body standard, legal certification, or security attestation.

## Start here

- [`guides/adoption.mdx`](./guides/adoption.mdx) — select the minimum justified profile and build one vertical slice.
- [`specification/index.mdx`](./specification/index.mdx) — normative scope, conformance profiles, and invariants.
- [`cheatsheets/architecture.mdx`](./cheatsheets/architecture.mdx) — canonical vocabulary and decision rules.
- [`reference/index.mdx`](./reference/index.mdx) — exact terms, interfaces, schemas, evidence expectations, API, and manifest profiles.
- [`handbook/runtime.mdx`](./handbook/runtime.mdx) — build the kernel, journal, effect ledger, leases, durable backend, recovery, and replay.
- [`handbook/ports-and-adapters.mdx`](./handbook/ports-and-adapters.mdx) — implement and verify a provider adapter.
- [`reference/conformance-checklist.mdx`](./reference/conformance-checklist.mdx) — assess cumulative profiles against reproducible evidence.

## Normative reading order

1. [`specification/resource-model.mdx`](./specification/resource-model.mdx) — stable resources and immutable versions.
2. [`specification/execution-model.mdx`](./specification/execution-model.mdx) — runs, activities, effects, invocations, retries, branches, iterations, and experiments.
3. [`specification/runtime.mdx`](./specification/runtime.mdx) — kernel, runtime service, durable execution, workers, leases, journal, and recovery.
4. [`specification/data-and-evidence.mdx`](./specification/data-and-evidence.mdx) — state, context, memory, artifacts, events, telemetry, audit, and lineage.
5. [`specification/platform.mdx`](./specification/platform.mdx) — planes, cells, tenancy, marketplace, and deployment.
6. [`specification/security-and-governance.mdx`](./specification/security-and-governance.mdx) — trust boundaries and controls.
7. [`specification/evaluation-and-conformance.mdx`](./specification/evaluation-and-conformance.mdx) — evaluation-driven development and conformance evidence.

## Canonical vocabulary

```text
Agent -> AgentVersion -> AgentRun
Workflow -> WorkflowVersion -> WorkflowRun
ExecutionPlan -> ExecutionPlanVersion -> ExecutionPlanRun

WorkflowRun
└── ActivityRun
    ├── ActivityAttempt
    ├── ExecutionBranch
    ├── Iteration
    └── Effect
        └── Invocation

WorkerLease
ExperimentRun -> ExperimentVariant -> ExperimentTrial -> WorkflowRunRef
```

`Run` is reserved for independently addressable durable executions. The core does not define unqualified `Step`, `Round`, `AttemptRun`, `TrialRun`, `SubAgent`, or `SubWorkflow`.

## Documentation site

Markdown/MDX is the source of truth; Mintlify renders the website. Navigation and compatibility redirects live in [`docs.json`](./docs.json).

```bash
npm install --global mint@4.2.687
mint dev
```

Validation:

```bash
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
mint validate
mint broken-links
```

## Repository map

```text
specification/  normative semantic specification
reference/      glossary, exact contracts, schemas, checklist, and profiles
guides/         adoption and reader pathways
handbook/       application, runtime, integration, security, and operations guides
evaluation/     evaluation-driven development and adapters
implementation/ module layout, rollout, testing, and resilience
patterns/       reusable composition patterns
examples/       worked end-to-end systems
decisions/      decision guide and ADRs
research/       primary evidence and comparisons
project/        documentation, release, and review governance
```

The [documentation architecture](./project/documentation-architecture.mdx) defines authority, page contracts, reader journeys, canonical ownership, navigation, quality, lifecycle, redirects, and change propagation. [Release and errata governance](./project/releases-and-errata.mdx) defines publication status, versioning, compatibility, and corrections.

## Contributing

A terminology or boundary change is incomplete until the specification, reference contracts, conformance evidence, schemas, guides, examples, diagrams, ADRs, cheatsheets, release notes, and automated checks agree. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`AGENTS.md`](./AGENTS.md).
