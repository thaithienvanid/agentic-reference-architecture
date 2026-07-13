#!/usr/bin/env python3
"""Deterministic consistency checks for ARA documentation and contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TABS = [
    "Specification",
    "Guides",
    "Reference",
    "Patterns & examples",
    "Project",
]

REQUIRED_SPECIFICATION_PAGES = [
    "specification/index",
    "specification/resource-model",
    "specification/execution-model",
    "specification/runtime",
    "specification/data-and-evidence",
    "specification/platform",
    "specification/security-and-governance",
    "specification/evaluation-and-conformance",
]

REQUIRED_REFERENCE_PAGES = [
    "reference/index",
    "reference/glossary",
    "reference/conventions",
    "reference/interfaces",
    "reference/events-and-state",
    "reference/conformance-checklist",
    "reference/api",
    "reference/manifests",
]

REQUIRED_PATHWAY_AND_GOVERNANCE_PAGES = [
    "guides/index",
    "guides/adoption",
    "handbook/runtime",
    "handbook/ports-and-adapters",
    "implementation/testing-and-resilience",
    "project/index",
    "project/documentation-architecture",
    "project/releases-and-errata",
    "project/review-history",
]

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

HOW_TO_CONTRACTS: dict[str, dict[str, Any]] = {
    "guides/adoption.mdx": {
        "required": ["## Outcome", "## Prerequisites", "## Validation"],
        "numbered_steps": 8,
    },
    "handbook/runtime.mdx": {
        "required": ["## Outcome", "## Prerequisites", "## Validation", "## Failure-injection suite"],
        "numbered_steps": 6,
    },
    "handbook/ports-and-adapters.mdx": {
        "required": ["## Outcome", "## Prerequisites", "## Validation"],
        "numbered_steps": 6,
    },
}

DOCUMENTATION_ARCHITECTURE_HEADINGS = [
    "## Research basis",
    "## Authority order",
    "## Reader-facing architecture",
    "## Documentation-mode mapping",
    "## Reader journeys",
    "## Page contracts",
    "## Canonical ownership",
    "## Duplication review",
    "## Content budgets",
    "## Change propagation",
    "## Navigation rules",
    "## Quality model",
    "## Content lifecycle and review triggers",
    "## Reader evidence and continuous improvement",
    "## Publication and errata",
    "## Quality gates",
]

CONFORMANCE_CHECKLIST_HEADINGS = [
    "## Purpose",
    "## Assessment record",
    "## ARA Core",
    "## ARA Durable",
    "## ARA Enterprise",
    "## ARA Marketplace",
    "## ARA Regulated",
    "## Evidence package structure",
    "## Review procedure",
    "## Validation",
]

RETIRED_TERMS = {
    r"\bAgentDefinition\b": "use Agent and AgentVersion",
    r"\bWorkflowDefinition\b": "use Workflow and WorkflowVersion",
    r"\bActivityDefinition\b": "use Activity inside WorkflowVersion",
    r"\bTrialRun\b": "use ExperimentTrial",
    r"\bIterationRun\b": "use Iteration",
    r"\bInvocationAttempt\b": "use Invocation",
    r"\bEffectRecord\b": "use Effect",
    r"\bAttemptRun\b": "use ActivityAttempt or Invocation",
    r"\bExecutionEpisode\b": "use WorkerLease",
    r"\bWorkflowEnginePort\b": "use DurableExecutionPort",
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

NORMATIVE_REFERENCE_FILES = {
    "reference/conventions.mdx",
    "reference/interfaces.mdx",
    "reference/events-and-state.mdx",
    "evaluation/gates-and-metrics.mdx",
}

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
    "never generic",
    "core does not define",
)

REQUIRED_REDIRECTS = {
    "/rfc": "/specification/index",
    "/rfc/index": "/specification/index",
    "/rfc/execution-model": "/specification/execution-model",
    "/rfc/runtime": "/specification/runtime",
    "/audits/documentation-architecture-2026-07-13": "/project/review-history",
    "/audits/refinement-report-2026-07-12": "/project/review-history",
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


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


def iter_groups(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if isinstance(value.get("group"), str):
            yield value
        for child in value.values():
            yield from iter_groups(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_groups(child)


def page_exists(page: str) -> bool:
    return (ROOT / f"{page}.mdx").exists() or (ROOT / f"{page}.md").exists()


def public_mdx_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.mdx")
        if ".git" not in path.parts and "_drafts" not in path.parts
    )


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def declares_normative_authority(text: str) -> bool:
    return bool(
        re.search(
            r"^>\s*\*\*Status:\s*Normative\b",
            text,
            flags=re.MULTILINE,
        )
    )


def is_explicit_negative_guidance(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in NEGATIVE_CONTEXT_MARKERS)


def check_how_to(rel: str, text: str, contract: dict[str, Any], failures: list[str]) -> None:
    if "Status: Informative how-to guide" not in text:
        fail(f"{rel}: missing Informative how-to guide status", failures)
    for heading in contract["required"]:
        if heading not in text:
            fail(f"{rel}: missing how-to section {heading}", failures)
    count = len(re.findall(r"^##\s+\d+\.", text, flags=re.MULTILINE))
    if count < contract["numbered_steps"]:
        fail(
            f"{rel}: needs at least {contract['numbered_steps']} numbered H2 steps; found {count}",
            failures,
        )


def parse_json_fences(path: Path, text: str, failures: list[str]) -> int:
    count = 0
    for index, body in enumerate(re.findall(r"```json\s*\n(.*?)\n```", text, flags=re.S), 1):
        count += 1
        try:
            json.loads(body)
        except json.JSONDecodeError as error:
            fail(f"{path.relative_to(ROOT)}: invalid JSON fence {index}: {error}", failures)
    return count


def main() -> int:
    failures: list[str] = []

    try:
        docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Unable to load docs.json: {error}")
        return 1

    pages = collect_pages(docs.get("navigation", {}))
    page_set = set(pages)

    duplicates = sorted({page for page in pages if pages.count(page) > 1})
    if duplicates:
        fail(f"duplicate navigation/root pages: {duplicates}", failures)

    for page in pages:
        if not page_exists(page):
            fail(f"navigation target missing: {page}", failures)

    files = public_mdx_files()
    nav_paths = {
        f"{page}.mdx" if (ROOT / f"{page}.mdx").exists() else f"{page}.md"
        for page in pages
        if page_exists(page)
    }
    file_paths = {path.relative_to(ROOT).as_posix() for path in files}
    orphans = sorted(file_paths - nav_paths)
    if orphans:
        fail(f"public MDX pages not in navigation: {orphans}", failures)

    json_fence_count = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        metadata = frontmatter(text)
        for field in ("title", "description"):
            if not metadata.get(field):
                fail(f"{rel}: missing frontmatter field {field}", failures)

        if declares_normative_authority(text) and not (
            rel.startswith("specification/") or rel in NORMATIVE_REFERENCE_FILES
        ):
            fail(f"{rel}: normative authority outside specification/reference owner", failures)

        if rel != "project/review-history.mdx":
            if re.search(r"\]\(/rfc(?:/[^)]*)?\)", text) or re.search(r'href="/rfc(?:/[^"]*)?"', text):
                fail(f"{rel}: live internal link uses retired /rfc path", failures)
            if re.search(r"`/?rfc/`", text):
                fail(f"{rel}: describes retired rfc/ as a live directory", failures)

        for pattern, guidance in RETIRED_TERMS.items():
            regex = re.compile(pattern)
            for line_number, line in enumerate(text.splitlines(), 1):
                if regex.search(line) and not is_explicit_negative_guidance(line):
                    fail(f"{rel}:{line_number}: retired term; {guidance}", failures)

        json_fence_count += parse_json_fences(path, text, failures)

    for retired_dir in ("rfc", "audits", "specifications", "standard"):
        if (ROOT / retired_dir).exists():
            fail(f"retired or competing documentation directory exists: {retired_dir}/", failures)

    for group in iter_groups(docs.get("navigation", {})):
        direct_pages = [item for item in group.get("pages", []) if isinstance(item, str)]
        if len(direct_pages) > 7:
            fail(f"navigation group {group['group']!r} has more than 7 direct pages", failures)
        root = group.get("root")
        if root is not None and not isinstance(root, str):
            fail(f"navigation group {group['group']!r} has a non-string root", failures)

    tabs = [
        item.get("tab")
        for item in docs.get("navigation", {}).get("tabs", [])
        if isinstance(item, dict)
    ]
    if tabs != EXPECTED_TABS:
        fail(f"navigation tabs must be exactly {EXPECTED_TABS}; found {tabs}", failures)

    redirects = docs.get("redirects", [])
    redirect_map: dict[str, str] = {}
    for item in redirects:
        if not isinstance(item, dict):
            fail(f"invalid redirect entry: {item!r}", failures)
            continue
        source = item.get("source")
        destination = item.get("destination")
        if not isinstance(source, str) or not source.startswith("/"):
            fail(f"invalid redirect source: {item!r}", failures)
            continue
        if not isinstance(destination, str) or not destination.startswith("/"):
            fail(f"invalid redirect destination: {item!r}", failures)
            continue
        if source in redirect_map:
            fail(f"duplicate redirect source: {source}", failures)
        redirect_map[source] = destination
        source_page = source.strip("/")
        destination_page = destination.strip("/")
        if page_exists(source_page):
            fail(f"redirect source shadows live page: {source}", failures)
        if destination_page not in page_set and not page_exists(destination_page):
            fail(f"redirect destination does not exist: {destination}", failures)

    for source, destination in REQUIRED_REDIRECTS.items():
        if redirect_map.get(source) != destination:
            fail(f"required redirect missing or wrong: {source} -> {destination}", failures)

    for page in (
        REQUIRED_SPECIFICATION_PAGES
        + REQUIRED_REFERENCE_PAGES
        + REQUIRED_PATHWAY_AND_GOVERNANCE_PAGES
    ):
        if page not in page_set:
            fail(f"required public page not in navigation: {page}", failures)

    manifests = (ROOT / "reference/manifests.mdx").read_text(encoding="utf-8")
    if re.search(r"\bamount:\s+[0-9]+(?:\.[0-9]+)?\b", manifests):
        fail("unquoted monetary amount in manifests", failures)

    for rel in GATE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        missing = [gate for gate in CANONICAL_GATES if gate not in text]
        if missing:
            fail(f"{rel}: missing canonical gates {missing}", failures)

    for rel in ("specification/runtime.mdx", "diagrams/index.mdx"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        for transition in ("Reconciling --> Running", "Reconciling --> Failed"):
            if transition not in text:
                fail(f"{rel}: missing state transition {transition}", failures)

    execution = (ROOT / "specification/execution-model.mdx").read_text(encoding="utf-8")
    for term in CANONICAL_EXECUTION_TERMS:
        if term not in execution:
            fail(f"execution model missing {term}", failures)

    specification = (ROOT / "specification/index.mdx").read_text(encoding="utf-8")
    for phrase in (
        "Normative candidate",
        "not an RFC Series publication",
        "commit or digest",
    ):
        if phrase not in specification:
            fail(f"specification/index.mdx missing publication phrase: {phrase}", failures)

    for rel, contract in HOW_TO_CONTRACTS.items():
        path = ROOT / rel
        if not path.exists():
            fail(f"required how-to page missing: {rel}", failures)
        else:
            check_how_to(rel, path.read_text(encoding="utf-8"), contract, failures)

    checklist = (ROOT / "reference/conformance-checklist.mdx").read_text(encoding="utf-8")
    for heading in CONFORMANCE_CHECKLIST_HEADINGS:
        if heading not in checklist:
            fail(f"conformance checklist missing section: {heading}", failures)
    for status in ("passed", "failed", "not_assessed", "not_applicable", "deviation_accepted"):
        if f"`{status}`" not in checklist:
            fail(f"conformance checklist missing status: {status}", failures)
    if "does not replace the normative" not in checklist:
        fail("conformance checklist must defer to the normative specification", failures)

    architecture = (ROOT / "project/documentation-architecture.mdx").read_text(encoding="utf-8")
    for heading in DOCUMENTATION_ARCHITECTURE_HEADINGS:
        if heading not in architecture:
            fail(f"documentation architecture missing section: {heading}", failures)
    for dimension in (
        "Correctness",
        "Findability",
        "Authority clarity",
        "Completeness",
        "Economy",
        "Reproducibility",
        "Maintainability",
    ):
        if dimension not in architecture:
            fail(f"documentation architecture missing quality dimension: {dimension}", failures)

    guides_index = (ROOT / "guides/index.mdx").read_text(encoding="utf-8")
    for target in (
        "/specification/index",
        "/handbook/runtime",
        "/handbook/ports-and-adapters",
        "/reference/conformance-checklist",
    ):
        if target not in guides_index:
            fail(f"guides/index.mdx missing task entry: {target}", failures)

    sources = (ROOT / "research/sources.mdx").read_text(encoding="utf-8")
    if "RFC Editor — What is an RFC?" not in sources:
        fail("research sources missing RFC Series terminology source", failures)

    if failures:
        print("Documentation consistency checks failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(
        "Documentation consistency checks passed for "
        f"{len(pages)} navigation/root pages, {len(files)} public MDX pages, "
        f"and {json_fence_count} JSON code fences."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
