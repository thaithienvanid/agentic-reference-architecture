# Agent instructions

## Objective

Maintain a concise, framework-agnostic, production-grade Agentic Reference Architecture. Markdown/MDX is the source of truth; Mintlify renders it.

## Authority order

1. `/rfc` and explicitly normative specification pages.
2. ADRs.
3. Informative guides and patterns.
4. Examples and research.

An informative page MUST NOT redefine a normative term.

## Canonical naming

- Stable identity: `Agent`, `Workflow`, `ExecutionPlan`, `Prompt`, `Tool`, `Policy`, `EvaluationSuite`.
- Immutable behavior: the corresponding `*Version` or `PackageRelease`.
- Independently durable execution: `*Run`.
- Workflow unit: `Activity`; execution: `ActivityRun`.
- Whole-activity restart: `ActivityAttempt`.
- Sequential intentional cycle: `Iteration`.
- Parallel candidate/path: `ExecutionBranch`.
- Logical external or nondeterministic operation: `Effect`.
- Concrete adapter/provider call: `Invocation`.
- Temporary worker ownership: `WorkerLease`.
- Experiment repetition: `ExperimentTrial` referencing a `WorkflowRun`.

Do not introduce unqualified `Step`, `Round`, `AttemptRun`, `TrialRun`, `SubAgent`, `SubWorkflow`, `ExecutionEpisode`, or provider-specific workflow-engine names into the normative core.

## Non-negotiable architecture rules

1. Models propose; deterministic code, policy, and humans authorize.
2. Stable identities, immutable versions, and executions are distinct.
3. Every production run pins an immutable deployment snapshot.
4. State, context, memory, artifacts, checkpoints, telemetry, audit, and usage remain separate.
5. Every external or nondeterministic operation is a typed effect recorded before dispatch.
6. Each concrete call is an invocation of exactly one effect.
7. Mutating effects define idempotency or reconciliation.
8. Child runs receive explicit reduced capabilities, budget, deadline, and result contracts.
9. Provider/framework DTOs stop at adapters.
10. Evaluation contracts and hard gates are part of deployable behavior.

## Writing

- Use BCP 14 uppercase terms only on normative pages.
- Use official primary sources for time-sensitive or vendor-specific claims.
- Label facts, inferences, and ARA recommendations.
- Explain ownership, forbidden ownership, failure behavior, testing, and trade-offs.
- Keep examples aligned with canonical schemas and names.
- Prefer links to the canonical rule over duplicated lists.

## Validation

Run:

```bash
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
mint validate
mint broken-links
```
