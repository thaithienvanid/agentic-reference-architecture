# Agent instructions for this repository

## Objective

Maintain a coherent, framework-agnostic Agentic Reference Architecture. Markdown/MDX is the source of truth; Mintlify renders the website.

## Non-negotiable architecture rules

1. Models propose; deterministic code, policy, and humans authorize.
2. Definition objects and execution objects have separate identities.
3. Published definitions are immutable and deployments pin exact versions/digests.
4. Workflow state, conversation, context, memory, artifacts, checkpoints, traces, audit, and usage are separate models.
5. Every external effect is typed, authorized, budgeted, recorded before dispatch, and has idempotency/reconciliation behavior.
6. Child agents have independent runs and explicit reduced capability grants.
7. Framework, provider, database, broker, cloud, and telemetry types remain in adapters.
8. Evaluation contracts are part of deployable behavior.
9. Persistent domain identities such as participants or cases are not agent runs.
10. Cross-run dependencies use immutable artifacts and explicit decisions.

## Writing and research

- Use official primary sources for product claims.
- Add retrieval dates to time-sensitive research pages.
- Label facts, inferences, and recommendations distinctly.
- Do not claim knowledge of undocumented private architecture.
- Make trade-offs and failure modes explicit.
- Keep diagrams readable without surrounding prose.
- Use typed pseudocode and concrete examples where useful.

## File conventions

- Every website page is `.mdx` with `title` and `description` frontmatter.
- Add every new public page to `docs.json`.
- Keep normative content in `handbook/`; implementation examples must not silently redefine the core.
- Update ADRs when a consequential decision changes.
- Preserve internal links when moving pages or add redirects in `docs.json`.

## Validation

Run with the current Mintlify CLI:

```bash
mint validate
mint broken-links
```
