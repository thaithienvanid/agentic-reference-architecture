# Contributing

## Change workflow

1. Identify the canonical RFC or specification that owns the concept.
2. Make the normative change first.
3. Update affected interfaces, schemas, ADRs, diagrams, examples, guides, and cheatsheets.
4. Add or update a deterministic consistency check when drift can be detected mechanically.
5. Run the complete documentation validation suite.
6. Explain compatibility and migration impact in the pull request.

## Content status

- `/rfc` and pages marked **Status: Normative** define ARA.
- Guides, patterns, examples, and research are informative.
- Historical audit pages may quote retired terminology but do not define it.

## Review checklist

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
- [ ] Navigation and links are valid.

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
