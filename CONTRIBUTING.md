# Contributing

## Change workflow

1. Identify the canonical owner in `project/documentation-architecture.mdx`.
2. Change normative semantics in `/rfc` first, when semantics actually change.
3. Change exact interfaces or representations in `/reference` and version affected contracts.
4. Record a consequential architectural decision or reversal in an ADR.
5. Update affected guides, diagrams, examples, manifests, evaluation gates, and cheatsheets.
6. Add or update deterministic checks when drift can be detected mechanically.
7. Preserve moved public URLs with `docs.json` redirects.
8. Run the complete validation suite and explain compatibility/migration impact in the pull request.

## Content classes

- `/rfc` contains normative semantic requirements.
- Explicitly marked pages in `/reference` contain normative lookup contracts.
- ADRs record accepted decisions and rationale.
- Guides explain how and why to apply the standard.
- Patterns provide reusable composition guidance.
- Examples illustrate the model but never create new requirements.
- Research records facts, inferences, comparisons, and sources.
- Audit pages are historical and may quote retired terminology.

Every public MDX page has `title` and `description` frontmatter. State the content status near the top when authority is not obvious.

## Review checklist

- [ ] The page has one primary purpose and correct content class.
- [ ] No lower-authority page redefines a canonical rule.
- [ ] Stable resource, immutable version, and runtime execution are distinct.
- [ ] `Run` is used only for an independently durable execution.
- [ ] Activity retry, iteration, branch, effect, invocation, and worker lease are not conflated.
- [ ] Inline composition and child execution are explicitly distinguished.
- [ ] Inputs, outputs, state transitions, tenant scope, budgets, and permissions are typed.
- [ ] Mutating effects have idempotency or reconciliation.
- [ ] Provider/framework types stop at adapters.
- [ ] Evaluation and observability impacts are covered.
- [ ] Security, data rights, and failure modes are covered.
- [ ] Migration or compatibility consequences are stated.
- [ ] Duplicated rule lists have been replaced with links where practical.
- [ ] Navigation, landing pages, redirects, and links are valid.

## Research

Use official documentation, specifications, source repositories, and primary papers. Record retrieval dates for time-sensitive claims. Do not attribute an ARA recommendation to a vendor unless the source states it.

## Validation

```bash
python scripts/check_doc_consistency.py
python -m json.tool docs.json > /dev/null
npm install --global mint@4.2.687
mint validate
mint broken-links
```
