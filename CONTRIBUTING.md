# Contributing

## Change workflow

1. Identify the canonical owner in `project/documentation-architecture.mdx`.
2. Classify the change as semantic, representation/profile, procedural, explanatory/editorial, navigation/redirect, research/evidence, or project history.
3. Change normative semantics in `/specification` first when meaning or conformance changes.
4. Change exact interfaces or representations in `/reference` and version affected contracts.
5. Update the conformance checklist and tests when evidence expectations or applicable requirements change.
6. Record a consequential architectural decision or reversal in an ADR.
7. Update affected guides, diagrams, examples, manifests, evaluation gates, and cheatsheets.
8. Add or update deterministic checks when drift can be detected mechanically.
9. Preserve moved public URLs with `docs.json` redirects; remove redirects that shadow live pages.
10. Classify release impact, compatibility, migration, and errata implications.
11. Run the complete validation suite and explain evidence and residual risk in the pull request.

## Content classes

- `/specification` contains normative semantic requirements and conformance profiles.
- Explicitly marked `/reference` pages contain normative lookup contracts.
- Reference profiles provide optional REST, manifest, or interoperability choices.
- Reference checklists map canonical requirements to implementation evidence without creating requirements.
- ADRs record accepted decisions and rationale.
- How-to guides lead to one verifiable adoption, implementation, integration, or operations outcome.
- Explanation guides teach concepts, alternatives, trade-offs, and failure modes.
- Patterns provide reusable composition guidance.
- Worked examples illustrate the model but never create requirements.
- Research records facts, inferences, recommendations, sources, and retrieval dates.
- Project review history consolidates prior findings without becoming current authority.

Every public MDX page has `title` and `description` frontmatter. State authority near the top when it could be ambiguous.

## Page-contract review

For a how-to guide, verify:

- [ ] The outcome and prerequisites are explicit.
- [ ] Actions or decisions are ordered and executable.
- [ ] Failure handling, security, and operational consequences are covered.
- [ ] Validation states how the reader proves completion.
- [ ] Exact semantics link to the canonical specification or reference owner.

For reference material, verify:

- [ ] Definitions, fields, interfaces, statuses, and constraints are optimized for lookup.
- [ ] Rationale and long procedures live elsewhere.
- [ ] Optional profiles are clearly distinguished from normative contracts.
- [ ] Checklist rows map to canonical owners and use closed assessment statuses.

For every public page, verify:

- [ ] It has one primary reader job and correct content class.
- [ ] A lower-authority page does not redefine a canonical rule.
- [ ] It remains useful when duplicated definitions are replaced by links.
- [ ] Navigation placement matches where the intended reader will look.
- [ ] Time-sensitive claims have primary sources and a review or retrieval date.

## Architecture review checklist

- [ ] Stable resource, immutable version, and runtime execution are distinct.
- [ ] `Run` is used only for independently durable execution.
- [ ] Activity retry, iteration, branch, effect, invocation, experiment trial, and worker lease are not conflated.
- [ ] Inline composition and child execution are explicitly distinguished.
- [ ] Inputs, outputs, state transitions, tenant scope, budgets, and permissions are typed.
- [ ] Mutating effects have idempotency or reconciliation.
- [ ] Provider and framework types stop at adapters.
- [ ] Evaluation, observability, audit, usage, and lineage impacts are covered.
- [ ] Security, data rights, failure modes, and recovery are covered.
- [ ] Migration, version, release, or errata consequences are stated.
- [ ] Duplicate rule lists are replaced with canonical links where practical.
- [ ] Navigation, landing pages, redirects, and links are valid.
- [ ] Conformance evidence reflects the deployed configuration and exact versions.

## Research

Use official documentation, specifications, source repositories, standards, and primary papers. Record retrieval dates for time-sensitive claims. Distinguish fact, inference, and ARA recommendation. Do not attribute an ARA recommendation to a vendor unless the source states it.

## Release governance

Follow `project/releases-and-errata.mdx`. Stable releases identify both semantic version and exact commit or digest. Never rewrite published meaning silently; use errata, migration notes, and explicit replacement versions.

A technical conformance claim also identifies the implementation release, deployment digest, claimed profiles, deviations, assessment date, and evidence-package reference.

## Validation

```bash
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
npm install --global mint@4.2.687
mint validate
mint broken-links
```
