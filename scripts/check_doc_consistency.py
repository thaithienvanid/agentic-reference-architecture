#!/usr/bin/env python3
"""Deterministic consistency checks for canonical ARA documentation contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_GATES = [
    "no_cross_tenant_access",
    "no_unauthorized_tool_execution",
    "no_approval_bypass",
    "approval_action_digest_matches",
    "no_duplicate_irreversible_effect",
    "no_forbidden_data_egress",
    "hard_budget_enforced",
    "mandatory_audit_complete",
]

GATE_FILES = [
    "evaluation/index.mdx",
    "evaluation/gates-and-metrics.mdx",
    "evaluation/evaluation-driven-development.mdx",
    "cheatsheets/evaluation.mdx",
]

# Historical audit records may quote retired terms. Normative and guidance pages may not.
VOCABULARY_EXCLUDED_PREFIXES = ("audits/",)
RETIRED_TERMS = {
    r"\bAgentDefinition\b": "use Agent for stable identity and AgentVersion for immutable behavior",
    r"\bWorkflowDefinition\b": "use Workflow for stable identity and WorkflowVersion for immutable behavior",
    r"\bActivityDefinition\b": "use Activity inside a WorkflowVersion and ActivityRun at runtime",
    r"\bTrialRun\b": "use ExperimentTrial in the experiment/evaluation bounded context",
    r"\bIterationRun\b": "use Iteration for an intentional subordinate execution cycle",
    r"\bInvocationAttempt\b": "use Invocation for one concrete adapter/provider call",
    r"\bEffectRecord\b": "use Effect for the logical external or nondeterministic operation",
    r"\bAttemptRun\b": "use the qualified ActivityAttempt or Invocation",
    r"\bExecutionEpisode\b": "use WorkerLease for temporary runtime ownership",
    r"\bWorkflowEnginePort\b": "use DurableExecutionPort for a backend-neutral durability boundary",
}

CANONICAL_EXECUTION_TERMS = [
    "AgentVersion",
    "WorkflowVersion",
    "ActivityRun",
    "ExecutionBranch",
    "Iteration",
    "ActivityAttempt",
    "Effect",
    "Invocation",
    "WorkerLease",
    "ExperimentTrial",
]


def collect_pages(value: Any) -> list[str]:
    pages: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "pages" and isinstance(child, list):
                pages.extend(item for item in child if isinstance(item, str))
            else:
                pages.extend(collect_pages(child))
    elif isinstance(value, list):
        for child in value:
            pages.extend(collect_pages(child))
    return pages


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def public_mdx_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.mdx")
        if ".git" not in path.parts
        and not path.relative_to(ROOT).as_posix().startswith(VOCABULARY_EXCLUDED_PREFIXES)
    )


def main() -> int:
    failures: list[str] = []
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    pages = collect_pages(docs.get("navigation", {}))

    duplicates = sorted({page for page in pages if pages.count(page) > 1})
    if duplicates:
        fail(f"duplicate navigation pages: {duplicates}", failures)

    for page in pages:
        if not ((ROOT / f"{page}.mdx").exists() or (ROOT / f"{page}.md").exists()):
            fail(f"navigation target missing: {page}", failures)

    files = public_mdx_files()
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in files)

    forbidden_literals = {
        "high-value-approval@5.0.0": "deprecated policy reference",
        "site.bundle.tar.gz": "obsolete bootstrap archive",
        "Kernel --> WorkflowPort": "non-canonical WorkflowPort name",
    }
    for token, reason in forbidden_literals.items():
        if token in corpus:
            fail(f"{reason}: {token}", failures)

    for pattern, guidance in RETIRED_TERMS.items():
        regex = re.compile(pattern)
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if regex.search(line):
                    fail(f"{rel}:{line_number}: retired term {regex.pattern!r}; {guidance}", failures)

    manifests = (ROOT / "specifications/manifests.mdx").read_text(encoding="utf-8")
    if re.search(r"\bamount:\s+[0-9]+(?:\.[0-9]+)?\b", manifests):
        fail("unquoted monetary amount in manifests", failures)

    for rel in GATE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        missing = [gate for gate in CANONICAL_GATES if gate not in text]
        if missing:
            fail(f"{rel} missing canonical gates: {missing}", failures)

    for rel in ["handbook/runtime.mdx", "diagrams/index.mdx"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for transition in ["Reconciling --> Running", "Reconciling --> Failed"]:
            if transition not in text:
                fail(f"{rel} missing state transition: {transition}", failures)

    ontology = (ROOT / "handbook/execution-ontology.mdx").read_text(encoding="utf-8")
    for term in CANONICAL_EXECUTION_TERMS:
        if term not in ontology:
            fail(f"execution ontology missing {term}", failures)

    if failures:
        print("Documentation consistency checks failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"Documentation consistency checks passed for {len(pages)} navigation pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
