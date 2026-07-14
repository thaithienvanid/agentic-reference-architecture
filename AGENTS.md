# Agent instructions

## Objective

Maintain a concise, framework-agnostic, production-grade Agentic Reference Architecture. Markdown/MDX explains the architecture; machine-readable artifacts under `contracts/` define exact representations for declared profiles; Mintlify renders the public site.

## Authority order

1. Normative semantic requirements in `/specification`.
2. Versioned machine-readable representations in `/contracts` for declared contract profiles.
3. Explicitly normative lookup material in `/reference`.
4. Accepted ADRs.
5. Informative guides and patterns.
6. Examples, research, and project review history.

ARA is an independent technical specification, not an RFC Series publication or a formal standards-body standard.

A lower-authority artifact MUST NOT redefine a higher-authority term or invariant. If prose and a named machine contract disagree about serialized shape, the machine contract controls that representation and the mismatch is recorded as an erratum. If a contract appears to change semantics, the specification controls.

Documentation authority, reader journeys, page contracts, quality criteria, and canonical ownership are defined in `project/documentation-architecture.mdx`. Publication, compatibility, and errata are governed by `project/releases-and-errata.mdx`.

## Content classes

- Specification: semantic requirements, ownership, invariants, modules, and conformance.
- Machine contract: exact schemas, registries, fixtures, and protocol representations.
- Normative reference: exact required terms, interfaces, lifecycle contracts, and mappings.
- Reference profile: optional REST, event, durable-backend, MCP, A2A, or manifest profile.
- Reference checklist: map requirements to evidence without adding semantics.
- How-to guide: outcome, prerequisites, ordered actions, failure handling, and validation.
- Explanation guide: concepts, alternatives, trade-offs, and failure modes.
- Pattern: reusable composition with use/avoid conditions.
- Worked example: end-to-end illustration only; no new requirements.
- Research: public facts, architectural inferences, ARA recommendations, sources, and review dates.
- Project review history: consolidated decisions and remediation; not current authority.

Every public MDX page has `title` and `description` frontmatter and states authority when ambiguity is possible.

## Canonical naming

- Stable identity: `Agent`, `Workflow`, `ExecutionPlan`, `Prompt`, `Tool`, `Policy`, `EvaluationSuite`, `HardGateRegistry`.
- Immutable behavior: corresponding `*Version` or `PackageRelease`.
- Independently durable execution: `*Run`.
- Workflow unit: `Activity`; execution: `ActivityRun`.
- Whole-activity restart: `ActivityAttempt`.
- Sequential intentional cycle: `Iteration`.
- Parallel candidate/path: `ExecutionBranch`.
- Logical external or nondeterministic operation: `Effect`.
- Concrete adapter/provider call: `Invocation`.
- Temporary worker ownership: `WorkerLease`.
- Independent experiment repetition: `ExperimentTrial` referencing an `ExecutionSubjectRef`.

The normative core does not define unqualified `Step`, `Round`, `AttemptRun`, `TrialRun`, `SubAgent`, `SubWorkflow`, `ExecutionEpisode`, or provider-specific durable-backend names.

## Non-negotiable architecture rules

1. Models propose; deterministic software, policy, resource authorization, and humans authorize.
2. Domain core, Shared Kernel, Application layer, Execution Kernel, Runtime Service, ports, and adapters remain distinct.
3. Stable identities, immutable versions, and executions are distinct.
4. Every production run pins an immutable `DeploymentSnapshot`.
5. `AgentRun` owns exactly one root `WorkflowRun`; inline agent activities create no independent agent run.
6. State, context, memory, artifacts, checkpoints, telemetry, audit, usage, and evaluation remain separate.
7. Every semantically material external or nondeterministic operation is an authorized `Effect` recorded before dispatch.
8. Each concrete call is an `Invocation` of exactly one effect.
9. Mutating effects define idempotency, reconciliation, or both.
10. Authoritative transition writes use one fenced atomic `ExecutionCommitPort` boundary.
11. Child runs receive explicitly attenuated capabilities, budget, deadline, cancellation, and result contracts.
12. Provider/framework DTOs stop at adapters; protocols do not replace local policy or execution truth.
13. Evaluation contracts and hard gates are part of deployable behavior.
14. Machine contracts, fixtures, registries, examples, and normative prose evolve together.

## Conformance modules

ARA Core is required. Other modules are composable:

```text
ARA Durable
ARA Multi-Tenant
ARA Enterprise Operations
ARA Marketplace
ARA High-Assurance
ARA Regulated
```

Do not describe these modules as one mandatory cumulative ladder. `ARA Enterprise` is only a convenience bundle defined by the specification.

## Writing and maintenance

- Use BCP 14 uppercase terms only in normative owners.
- Use official primary sources for time-sensitive, protocol, vendor, security, legal, or standards claims.
- Label facts, inferences, and ARA recommendations.
- Give each page one primary reader job and one content class.
- Make how-to pages verifiable: outcome, prerequisites, ordered procedure, failure handling, and validation.
- Keep reference pages compact; move rationale to guides or ADRs.
- Keep examples aligned with executable fixtures and canonical names.
- Prefer canonical links or generated snippets over duplicated complete definitions.
- Preserve moved URLs through `docs.json` redirects; never let a redirect shadow a live page.
- Update specification, contracts, reference, checklist, diagrams, examples, ADRs, release notes, and tests together when semantics change.
- Record reviewed versions and dates for time-sensitive sources.
- Do not call ARA Stable without the evidence required by `project/releases-and-errata.mdx`.

## Validation

```bash
python -m pip install --requirement requirements-docs.txt
python scripts/check_contracts.py
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
npm install --global mint@4.2.687
mint validate
mint broken-links
```

A change is incomplete while any semantic owner, machine contract, page contract, navigation path, compatibility note, conformance evidence path, or deterministic drift check remains inconsistent.
