# Agentic Reference Architecture

A framework-agnostic, evaluation-driven reference architecture for production AI agents, deterministic and agentic workflows, long-running execution, multi-agent systems, enterprise SaaS platforms, and governed marketplaces.

> **Models propose. Deterministic software, policy, and humans authorize. The runtime executes, persists, and audits.**

## Source of truth

All documentation is maintained as Markdown/MDX in this repository and rendered as a Mintlify site. The site configuration is [`docs.json`](./docs.json).

## Deliverables

- Architecture handbook
- Architecture cheatsheet
- Evaluation-driven development handbook
- Evaluation cheatsheet
- Pattern catalog
- Architecture decision guide and ADRs
- Reference interfaces
- Mermaid diagram pack
- API, event, state, and manifest specifications
- DDD modeling guide
- Worked procurement and synthetic-research examples
- Research findings, comparisons, and primary-source index
- Implementation roadmap and architecture variants

See [`deliverables.mdx`](./deliverables.mdx) for the navigation map.

## Local preview

Install the current Mintlify CLI and run:

```bash
npm install -g mint
mint dev
```

Quality checks:

```bash
mint validate
mint broken-links
```

Current Mintlify setup follows the official [`docs.json` configuration](https://www.mintlify.com/docs/organize/settings), [navigation](https://www.mintlify.com/docs/organize/navigation), and [Mermaid](https://www.mintlify.com/docs/components/mermaid-diagrams) documentation.

## Repository structure

```text
handbook/        normative architecture
cheatsheets/     compact operational references
evaluation/      evaluation-driven development and adapters
patterns/        reusable workflow and multi-agent patterns
decisions/       decision guide and ADRs
specifications/  interfaces, APIs, manifests, events, and schemas
diagrams/        standalone Mermaid diagram pack
examples/        end-to-end worked examples
research/        primary evidence and comparison matrices
implementation/  rollout and architecture variants
```

## Contribution principles

1. Keep the framework-independent core free of provider SDK types.
2. Distinguish documented facts, architectural inferences, and ARA recommendations.
3. Prefer official documentation, specifications, repositories, and primary papers.
4. Update affected contracts, diagrams, examples, and ADRs together.
5. Treat prompts, policies, workflows, agents, tools, and evaluators as immutable versioned assets after publication.
6. Add new domain concepts as bounded-context extensions rather than expanding the shared core without evidence.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`AGENTS.md`](./AGENTS.md).
