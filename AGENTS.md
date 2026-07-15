# Agent instructions

## Objective

Maintain a concise, framework-neutral, internally consistent Agentic Reference Architecture.

## Authority order

1. Normative semantics under `specification/`.
2. Versioned machine contracts under `contracts/`.
3. Normative lookup material under `reference/`.
4. Accepted decisions under `project/architecture-decisions.mdx`.
5. Informative guides, patterns, and examples.

A lower-authority artifact must not redefine a higher-authority concept.

## Canonical model

```text
Resource -> immutable ResourceVersion -> DeploymentSnapshot

Run
├── RunAuthority
├── compact RunHeader
├── ordered inputs and semantic events
└── ActivityRun
    ├── optional ActivityAttempt
    ├── optional execution scope: branch / iteration
    ├── DurableCommand
    └── Effect
        └── Invocation
```

## Non-negotiable rules

1. One Run has exactly one sequenced execution authority.
2. `AgentRun`, `WorkflowRun`, and `ExecutionPlanRun` are typed views of `Run`, not mandatory wrapper aggregates.
3. Timers, signal waits, local child starts, continuation, checkpoints, and cancellation are `DurableCommand`s, not Effects.
4. An `Effect` is a semantically material external or nondeterministic operation.
5. An `Invocation` is one concrete provider or adapter call for an Effect.
6. The default database profile uses a compact header plus append-only log; it does not rewrite an ever-growing complete state object.
7. Mutating Effects define idempotency, reconciliation, or both.
8. Human approval is an action-bound `ApprovalCase`; notification delivery is an Effect.
9. Runtime authority, invocation authority, read authority, and principal identity use separate context types.
10. Optional capabilities stay optional. Marketplace, memory, sandbox, external-agent federation, multi-region cells, and regulated controls are extensions.

## Validation

```bash
python -m pip install --requirement requirements-docs.txt
python scripts/check_contracts.py
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
mint validate
mint broken-links
```

A semantic change is incomplete until specification, contracts, reference, examples, migration guidance, navigation, and deterministic checks agree.
