# Contributing

## Documentation workflow

1. Create a branch.
2. Edit or add MDX pages with `title` and `description` frontmatter.
3. Add new pages to `docs.json` navigation.
4. Use Mermaid for architecture diagrams and make each diagram independently understandable.
5. Run `mint validate` and `mint broken-links` with the current Mintlify CLI.
6. Open a pull request that explains the architectural change, affected contracts, trade-offs, and migration impact.

## Content standards

- Use precise complete sentences.
- Define terms before relying on them.
- Keep definition-time concepts separate from runtime executions.
- Distinguish workflow state, conversation, working context, memory, artifacts, checkpoints, traces, and audit.
- Describe why a component exists, what it owns, what it must not own, dependencies, failure modes, testing, and an example.
- Prefer deterministic software when agentic choice is unnecessary.
- Do not present model behavior as a business invariant.
- Do not expose private chain-of-thought; document observable plans, decisions, actions, evidence, and outcomes.

## Research standards

- Use official documentation, source repositories, specifications, and primary papers.
- Include retrieval dates for time-sensitive product claims.
- Mark private-architecture assumptions as inference.
- Separate vendor facts from ARA recommendations.
- Avoid popularity-based ranking; compare against explicit criteria.

## Review checklist

- [ ] Source dependencies still point inward.
- [ ] Provider/framework DTOs stop at adapters.
- [ ] Side effects have idempotency and reconciliation semantics.
- [ ] Tenant and data boundaries are explicit.
- [ ] Evaluation and observability impacts are covered.
- [ ] Security and failure modes are described.
- [ ] Versioning and migration effects are described.
- [ ] Diagrams, examples, ADRs, and navigation are synchronized.
