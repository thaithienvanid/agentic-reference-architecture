# Agent instructions

## Objective

Maintain a concise, framework-agnostic, production-grade Agentic Reference Architecture. Markdown/MDX is the source of truth; Mintlify renders it.

## Authority order

1. Normative semantic rules in `/rfc`.
2. Explicitly normative contracts in `/reference`.
3. Accepted ADRs.
4. Informative guides and patterns.
5. Examples, research, and audit history.

A lower-authority page MUST NOT redefine a higher-authority term or rule. Prefer a link to the canonical owner over copying a list.

The documentation authority and page taxonomy are defined in `project/documentation-architecture.mdx`.

## Page types

- RFC: semantic requirements and conformance.
- Reference: exact terms, fields, interfaces, schemas, API and manifest profiles.
- Guide: how and why to apply the standard.
- Pattern: reusable composition with use/avoid conditions.
- Example: illustration only; no new rules.
- Research: evidence, inference, and comparison.
- Audit/history: historical findings and remediation.

Every public MDX page has `title` and `description` frontmatter. State the page’s status near the top when authority could be ambiguous.

## Canonical naming

- Stable identity: `Agent`, `Workflow`, `ExecutionPlan`, `Prompt`, `Tool`, `Policy`, `EvaluationSuite`.
- Immutable behavior: corresponding `*Version` or `PackageRelease`.
- Independently durable execution: `*Run`.
- Workflow unit: `Activity`; execution: `ActivityRun`.
- Whole-activity restart: `ActivityAttempt`.
- Sequential intentional cycle: `Iteration`.
- Parallel candidate/path: `ExecutionBranch`.
- Logical external or nondeterministic operation: `Effect`.
- Concrete adapter/provider call: `Invocation`.
- Temporary worker ownership: `WorkerLease`.
- Experiment repetition: `ExperimentTrial` referencing a `WorkflowRun`.

Do not introduce unqualified `Step`, `Round`, `AttemptRun`, `TrialRun`, `SubAgent`, `SubWorkflow`, `ExecutionEpisode`, or provider-specific durable-backend names into the normative core.

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

## Writing and maintenance

- Use BCP 14 uppercase terms only on normative pages.
- Use official primary sources for time-sensitive or vendor-specific claims.
- Label facts, inferences, and ARA recommendations.
- Explain ownership, forbidden ownership, failure behavior, testing, and trade-offs.
- Keep examples aligned with canonical schemas and names.
- Keep reference pages descriptive and compact; move rationale to guides or ADRs.
- Preserve moved URLs through `docs.json` redirects.
- Update the RFC, reference contracts, diagrams, examples, ADRs, and checks together when semantics change.

## Validation

Run:

```bash
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
mint validate
mint broken-links
```
