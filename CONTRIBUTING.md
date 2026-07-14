# Contributing

## Change workflow

1. Identify the canonical semantic owner in `project/documentation-architecture.mdx`.
2. Classify the change as semantic, machine-contract, reference/profile, procedural, explanatory/editorial, navigation/redirect, research/evidence, or project history.
3. Change `/specification` first when architectural meaning or conformance changes.
4. Change `/contracts` when exact serialized representation changes; version affected schemas, registries, profiles, and fixtures.
5. Update normative `/reference` material and compatibility rules.
6. Update the conformance checklist and tests when requirements, modules, profiles, or evidence expectations change.
7. Record a consequential decision or reversal in an ADR.
8. Update affected guides, diagrams, examples, manifests, evaluation gates, and cheatsheets.
9. Add or strengthen deterministic checks when drift can be detected mechanically.
10. Preserve moved public URLs with `docs.json` redirects and remove redirects that shadow live pages.
11. Classify release, migration, compatibility, and errata impact.
12. Run the complete validation suite and describe evidence and residual risk in the pull request.

## Content classes

- `/specification` owns normative semantic requirements and composable conformance modules.
- `/contracts` owns exact machine-readable representation for declared contract/profile versions.
- Explicitly marked `/reference` pages own normative lookup contracts or optional profiles.
- Reference checklists map canonical requirements to evidence without creating requirements.
- ADRs record accepted decisions and rationale.
- How-to guides lead to one verifiable adoption, implementation, integration, or operations outcome.
- Explanation guides teach concepts, alternatives, trade-offs, and failure modes.
- Patterns provide reusable composition guidance.
- Worked examples illustrate the model but never create requirements.
- Research records public facts, architectural inferences, ARA recommendations, sources, versions, and review dates.
- Project review history consolidates prior findings without becoming current authority.

Every public MDX page has `title` and `description` frontmatter and states authority when it could be ambiguous.

## Machine-contract review

For every schema or protocol change, verify:

- [ ] JSON Schema, OpenAPI, or AsyncAPI syntax is valid.
- [ ] `$id`, contract version, required/optional fields, and extension points are explicit.
- [ ] Every fixture validates against its matching schema.
- [ ] Registered event, effect, error, gate, and module identifiers are unique and versioned.
- [ ] Digests, money, time, duration, identifiers, and enum values follow canonical conventions.
- [ ] Sensitive payloads, credentials, and private hidden reasoning are excluded.
- [ ] Compatibility and migration behavior is documented.
- [ ] Prose snippets match the executable contract or link to it instead of diverging.

## Page-contract review

For a how-to guide, verify:

- [ ] Outcome and prerequisites are explicit.
- [ ] Actions or decisions are ordered and executable.
- [ ] Failure, security, and operational consequences are covered.
- [ ] Validation states how completion is proven.
- [ ] Exact semantics link to the canonical specification or reference owner.

For reference material, verify:

- [ ] Definitions, fields, interfaces, statuses, and constraints are optimized for lookup.
- [ ] Rationale and long procedures live elsewhere.
- [ ] Optional profiles are clearly distinguished from normative contracts.
- [ ] Checklist rows map to canonical owners and use closed assessment statuses.

For every public page, verify:

- [ ] It has one primary reader job and the correct content class.
- [ ] A lower-authority artifact does not redefine a canonical rule.
- [ ] It remains useful when duplicated definitions are replaced by links or generated examples.
- [ ] Navigation placement matches where the intended reader will look.
- [ ] Time-sensitive claims have primary sources, reviewed versions, and dates.

## Architecture review checklist

- [ ] Domain core, Shared Kernel, Application layer, Execution Kernel, Runtime Service, ports, and adapters are distinct.
- [ ] Stable resource, immutable version, and runtime execution are distinct.
- [ ] `AgentRun` maps to exactly one root `WorkflowRun`.
- [ ] `Run` is used only for independently durable execution.
- [ ] Activity retry, iteration, branch, effect, invocation, experiment trial, and worker lease are not conflated.
- [ ] `ExecutionIntent`, `RuntimeControlOperation`, `Effect`, and `Invocation` are distinguished.
- [ ] Parallel and repeated work uses execution-instance identity and deterministic joins.
- [ ] Authoritative transition writes are atomic and fenced.
- [ ] Mutating effects have stable semantic identity plus idempotency or reconciliation.
- [ ] Inline composition and child execution are explicitly distinguished.
- [ ] Inputs, outputs, state transitions, tenant scope, budgets, capabilities, and data policy are typed.
- [ ] Credentials are injected at dispatch rather than returned to core state.
- [ ] Provider and framework types stop at adapters.
- [ ] Evaluation, observability, audit, usage, lineage, and data rights are covered separately.
- [ ] Security, failure modes, recovery, and residual risk are explicit.
- [ ] Migration, version, release, and errata consequences are stated.
- [ ] Conformance evidence reflects the deployed configuration and exact contract versions.

## Conformance language

ARA Core is required; Durable, Multi-Tenant, Enterprise Operations, Marketplace, High-Assurance, and Regulated are composable modules. Do not describe them as one mandatory cumulative profile ladder.

`deviation_accepted` is not full conformance. A missing or unavailable required hard-gate evaluator produces `inconclusive` or `failed` according to the declared policy.

## Research

Use official documentation, specifications, source repositories, standards, and primary papers. Record retrieval/review dates and product or protocol versions for time-sensitive claims. Distinguish public fact, architectural inference, and ARA recommendation. Do not attribute an ARA recommendation to a vendor unless the source states it.

## Release governance

Follow `project/releases-and-errata.mdx`. Candidate and Stable are different evidence states. Stable releases identify semantic version, exact publication commit or digest, contract-tree digest, validation evidence, implementation evidence, independent review, and open errata.

Never rewrite published meaning silently; use errata, migration notes, and explicit replacement versions.

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
