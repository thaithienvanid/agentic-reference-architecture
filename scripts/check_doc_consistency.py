#!/usr/bin/env python3
"""Deterministic consistency checks for ARA documentation architecture and contracts."""

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

REQUIRED_RFC_PAGES = [
    "rfc/index",
    "rfc/resource-model",
    "rfc/execution-model",
    "rfc/runtime",
    "rfc/data-and-evidence",
    "rfc/platform",
    "rfc/security-and-governance",
    "rfc/evaluation-and-conformance",
]

REQUIRED_REFERENCE_PAGES = [
    "reference/index",
    "reference/glossary",
    "reference/conventions",
    "reference/interfaces",
    "reference/events-and-state",
    "reference/api",
    "reference/manifests",
]

REQUIRED_LANDING_PAGES = [
    "guides/index",
    "project/index",
    "project/documentation-architecture",
]

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

NEGATIVE_CONTEXT_MARKERS = (
    "does not define",
    "do not define",
    "do not create",
    "must not define",
    "retired",
    "legacy",
    "migration",
    "non-canonical",
    "alternatives:",
    "not `",
    "never generic",
    "core does not define",
)

NORMATIVE_REFERENCE_FILES = {
    "reference/conventions.mdx",
    "reference/interfaces.mdx",
    "reference/events-and-state.mdx",
    "evaluation/gates-and-metrics.mdx",
}


def collect_pages(value: Any) -> list[str]:
    pages: list[str] = []
    if isinstance(value, dict):
        root = value.get("root")
        if isinstance(root, str):
            pages.append(root)
        for key, child in value.items():
            if key == "pages" and isinstance(child, list):
                pages.extend(item for item in child if isinstance(item, str))
            elif key != "root":
                pages.extend(collect_pages(child))
    elif isinstance(value, list):
        for child in value:
            pages.extend(collect_pages(child))
    return pages


def iter_groups(value: Any):
    if isinstance(value, dict):
        if isinstance(value.get("group"), str):
            yield value
        for child in value.values():
            yield from iter_groups(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_groups(child)


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def public_mdx_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.mdx")
        if ".git" not in path.parts and "_drafts" not in path.parts
    )


def is_explicit_negative_guidance(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in NEGATIVE_CONTEXT_MARKERS)


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def declares_normative_authority(text: str) -> bool:
    """Match an actual status declaration, not quoted examples or prose."""
    return bool(
        re.search(
            r"^>\s*\*\*Status:\s*Normative(?:\s+reference)?(?:\s*·[^*]*)?\*\*",
            text,
            flags=re.MULTILINE,
        )
    )


def main() -> int:
    failures: list[str] = []
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    pages = collect_pages(docs.get("navigation", {}))

    duplicates = sorted({page for page in pages if pages.count(page) > 1})
    if duplicates:
        fail(f"duplicate navigation/root pages: {duplicates}", failures)

    for page in pages:
        if not ((ROOT / f"{page}.mdx").exists() or (ROOT / f"{page}.md").exists()):
            fail(f"navigation target missing: {page}", failures)

    nav_paths = {f"{page}.mdx" for page in pages}
    files = public_mdx_files()
    file_paths = {path.relative_to(ROOT).as_posix() for path in files}
    orphans = sorted(file_paths - nav_paths)
    if orphans:
        fail(f"public MDX pages not present in navigation: {orphans}", failures)

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        metadata = frontmatter(text)
        for field in ("title", "description"):
            if not metadata.get(field):
                fail(f"{rel}: missing frontmatter field {field}", failures)
        if "ndescription:" in text:
            fail(f"{rel}: malformed ndescription frontmatter", failures)

    for group in iter_groups(docs.get("navigation", {})):
        direct_pages = [item for item in group.get("pages", []) if isinstance(item, str)]
        if len(direct_pages) > 7:
            fail(f"navigation group {group['group']!r} has more than 7 direct pages", failures)

    redirects = docs.get("redirects", [])
    redirect_sources = [item.get("source") for item in redirects if isinstance(item, dict)]
    duplicate_redirects = sorted({source for source in redirect_sources if redirect_sources.count(source) > 1})
    if duplicate_redirects:
        fail(f"duplicate redirect sources: {duplicate_redirects}", failures)

    corpus = "\n".join(path.read_text(encoding="utf-8") for path in files)
    forbidden_literals = {
        "high-value-approval@5.0.0": "deprecated policy reference",
        "site.bundle.tar.gz": "obsolete bootstrap archive",
        "Kernel --> WorkflowPort": "non-canonical WorkflowPort name",
        "/specifications/": "retired public specifications path",
        "ARA v2": "retired baseline name",
    }
    for token, reason in forbidden_literals.items():
        if token in corpus:
            fail(f"{reason}: {token}", failures)

    if (ROOT / "specifications").exists():
        fail("retired specifications/ directory still exists", failures)

    for pattern, guidance in RETIRED_TERMS.items():
        regex = re.compile(pattern)
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            if rel.startswith("audits/"):
                continue
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if regex.search(line) and not is_explicit_negative_guidance(line):
                    fail(f"{rel}:{line_number}: retired term {regex.pattern!r}; {guidance}", failures)

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if declares_normative_authority(text) and not (
            rel.startswith("rfc/") or rel in NORMATIVE_REFERENCE_FILES
        ):
            fail(f"{rel}: normative authority outside RFC/reference owner", failures)

    manifests = (ROOT / "reference/manifests.mdx").read_text(encoding="utf-8")
    if re.search(r"\bamount:\s+[0-9]+(?:\.[0-9]+)?\b", manifests):
        fail("unquoted monetary amount in manifests", failures)

    for rel in GATE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        missing = [gate for gate in CANONICAL_GATES if gate not in text]
        if missing:
            fail(f"{rel} missing canonical gates: {missing}", failures)

    for rel in ["rfc/runtime.mdx", "diagrams/index.mdx"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for transition in ["Reconciling --> Running", "Reconciling --> Failed"]:
            if transition not in text:
                fail(f"{rel} missing state transition: {transition}", failures)

    ontology = (ROOT / "rfc/execution-model.mdx").read_text(encoding="utf-8")
    for term in CANONICAL_EXECUTION_TERMS:
        if term not in ontology:
            fail(f"execution model missing {term}", failures)

    for page in REQUIRED_RFC_PAGES + REQUIRED_REFERENCE_PAGES + REQUIRED_LANDING_PAGES:
        if page not in pages:
            fail(f"required public page not in navigation: {page}", failures)

    if failures:
        print("Documentation consistency checks failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(
        "Documentation consistency checks passed for "
        f"{len(pages)} navigation/root pages and {len(files)} public MDX pages."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
