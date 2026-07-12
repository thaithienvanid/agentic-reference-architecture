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

    corpus = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ROOT.rglob("*.mdx")
        if ".git" not in path.parts
    )

    forbidden = {
        "high-value-approval@5.0.0": "deprecated policy reference",
        "site.bundle.tar.gz": "obsolete bootstrap archive",
        "Kernel --> WorkflowPort": "non-canonical WorkflowPort name",
    }
    for token, reason in forbidden.items():
        if token in corpus:
            fail(f"{reason}: {token}", failures)

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

    required_terms = [
        "EffectRecord",
        "InvocationAttempt",
        "TrialRun",
        "IterationRun",
        "ExecutionBranch",
    ]
    ontology = (ROOT / "handbook/execution-ontology.mdx").read_text(encoding="utf-8")
    for term in required_terms:
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
