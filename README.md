# Agentic Reference Architecture

**ARA** is a framework-neutral reference architecture for production agentic applications and durable workflows.

The architecture deliberately keeps the mandatory core small:

```text
immutable definitions
+ one durable Run
+ one sequenced execution authority
+ typed activities
+ DurableCommands for orchestration
+ Effects and Invocations for external work
+ explicit authorization, evidence, and evaluation
```

Start with the [specification](specification/index.mdx), then use the [minimal internal application guide](guides/minimal-internal-app.mdx) for an implementation-sized profile.

> **Models propose. Deterministic software, policy, resource authorization, and humans authorize. The runtime executes, persists, and records.**

Status: **ARA 1.0 Release Candidate**. This repository is an independent technical specification, not a standards-body publication, legal certification, security attestation, or proof of operational effectiveness.
