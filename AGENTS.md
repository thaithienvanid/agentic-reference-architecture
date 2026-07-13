# Agent instructions

## Objective

Maintain a concise, framework-agnostic, production-grade Agentic Reference Architecture. Markdown/MDX is the source of truth; Mintlify renders it.

## Authority order

1. Normative semantic requirements in `/specification`.
2. Explicitly normative contracts in `/reference`.
3. Accepted ADRs.
4. Informative guides and patterns.
5. Examples, research, and project review history.

ARA is an independent technical specification, not an RFC Series publication or a formal standards-body standard.

A lower-authority page MUST NOT redefine a higher-authority term or rule. Prefer a link to the canonical owner over copying a complete definition.

Documentation authority, reader journeys, page contracts, quality criteria, and canonical ownership are defined in `project/documentation-architecture.mdx`. Publication, versioning, and errata are governed by `project/releases-and-errata.mdx`.

## Page types

- Specification: semantic requirements, ownership, invariants, profiles, and conformance.
- Normative reference: exact required terms, fields, interfaces, schemas, and wire representations.
- Reference profile: optional REST, manifest, or interoperability profile.
- Reference checklist: map canonical requirements to evidence without adding semantics.
- How-to guide: outcome, prerequisites, ordered actions, failure handling, and validation.
- Explanation guide: concepts, alternatives, trade-offs, and failure modes.
- Pattern: reusable composition with use/avoid conditions.
- Worked example: end-to-end illustration only; no new rules.
- Research: facts, inferences, recommendations, sources, and retrieval dates.
- Project review history: consolidated decisions and remediation; not current authority.

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
- Independent experiment repetition: `ExperimentTrial` referencing a `WorkflowRun`.

The normative core does not define unqualified `Step`, `Round`, `AttemptRun`, `TrialRun`, `SubAgent`, `SubWorkflow`, `ExecutionEpisode`, or provider-specific durable-backend names.

## Non-negotiable architecture rules

1. Models propose; deterministic code, policy, and humans authorize.
2. Stable identities, immutable versions, and executions are distinct.
3. Every production run pins an immutable deployment snapshot.
4. State, context, memory, artifacts, checkpoints, telemetry, audit, usage, and evaluation remain separate.
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
- Give each page one primary reader job and one content class.
- Make how-to pages verifiable: outcome, prerequisites, ordered procedure, failure handling, and validation.
- Keep reference pages compact; move rationale to guides or ADRs.
- Keep checklists traceable to canonical owners and explicit about assessment status.
- Explain ownership, forbidden ownership, failure behavior, security, evaluation, and trade-offs.
- Keep examples aligned with canonical schemas and names.
- Prefer canonical links over duplicated complete rule lists.
- Preserve moved URLs through `docs.json` redirects; never let a redirect shadow a live page.
- Update the specification, reference contracts, checklist, diagrams, examples, ADRs, release notes, and checks together when semantics change.
- Record retrieval or review dates for time-sensitive vendor, protocol, legal, security, and documentation-platform claims.

## Validation

```bash
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
mint validate
mint broken-links
```

A documentation change is incomplete while any page contract, navigation path, canonical owner, compatibility note, conformance evidence path, or automated drift check remains inconsistent.