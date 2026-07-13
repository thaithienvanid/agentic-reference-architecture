# Agentic Reference Architecture

A framework-agnostic, evaluation-driven standard for production AI agents, deterministic and agentic workflows, durable execution, multi-agent systems, enterprise platforms, and governed marketplaces.

> **Models propose. Deterministic software, policy, and humans authorize. The runtime executes, persists, and records.**

## Start with the standard

The normative semantic core is intentionally compact:

1. [`rfc/index.mdx`](./rfc/index.mdx) — scope, BCP 14 language, profiles, invariants.
2. [`rfc/resource-model.mdx`](./rfc/resource-model.mdx) — stable resources and immutable versions.
3. [`rfc/execution-model.mdx`](./rfc/execution-model.mdx) — runs, activities, effects, invocations, retries, branches, iterations, and experiments.
4. [`rfc/runtime.mdx`](./rfc/runtime.mdx) — kernel, runtime service, durable execution, workers, leases, journal, and recovery.
5. [`rfc/data-and-evidence.mdx`](./rfc/data-and-evidence.mdx) — state, context, memory, artifacts, events, telemetry, audit, and lineage.
6. [`rfc/platform.mdx`](./rfc/platform.mdx) — planes, cells, tenancy, marketplace, and deployment.
7. [`rfc/security-and-governance.mdx`](./rfc/security-and-governance.mdx) — trust boundaries and controls.
8. [`rfc/evaluation-and-conformance.mdx`](./rfc/evaluation-and-conformance.mdx) — evaluation-driven development and conformance profiles.

Exact names, interfaces, schemas, API conventions, and manifests live under [`reference/`](./reference/). The remaining sections provide informative guides, patterns, worked examples, implementation guidance, research, and project history.

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

Markdown/MDX is the source of truth; Mintlify renders the website. Navigation and redirects are defined in [`docs.json`](./docs.json).

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
rfc/             normative semantic standard
reference/       glossary, exact contracts, schemas, API and manifest profiles
guides/          section landing pages
handbook/        informative application, runtime, and platform guides
evaluation/      evaluation-driven development and adapters
patterns/        reusable composition patterns
examples/        worked end-to-end systems
implementation/  module layout, rollout, testing, and resilience
decisions/       decision guide and ADRs
research/        primary evidence and comparisons
project/         documentation governance and project overview
audits/          historical audit reports
```

The [documentation architecture](./project/documentation-architecture.mdx) defines authority, page types, canonical ownership, navigation, redirects, and change propagation.

## Contributing

A terminology or boundary change is incomplete until the RFC, reference contracts, schemas, examples, diagrams, ADRs, cheatsheets, and automated checks agree. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`AGENTS.md`](./AGENTS.md).
