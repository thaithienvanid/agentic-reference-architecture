#!/usr/bin/env python3
"""Validate ARA machine-readable contracts, registries, fixtures, and documentation examples."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
SCHEMAS = CONTRACTS / "schemas"
EXAMPLES = CONTRACTS / "examples"
REGISTRIES = CONTRACTS / "registries"
OPENAPI = CONTRACTS / "openapi" / "ara-api-profile.yaml"
ASYNCAPI = CONTRACTS / "asyncapi" / "ara-events-profile.yaml"

DIGEST_RE = re.compile(r"^sha256:[A-Fa-f0-9]{64}$")
EVENT_ID_RE = re.compile(r"^[a-z][a-z0-9_.-]*$")
GATE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def walk_values(value: Any, pointer: str = "$") -> Iterable[tuple[str, Any]]:
    yield pointer, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_values(child, f"{pointer}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_values(child, f"{pointer}[{index}]")


def validate_sha256_strings(path: Path, value: Any, failures: list[str], *, context: str = "") -> None:
    prefix = f" {context}" if context else ""
    for pointer, child in walk_values(value):
        if isinstance(child, str) and child.startswith("sha256:") and not DIGEST_RE.fullmatch(child):
            fail(
                f"{path.relative_to(ROOT)}{prefix} {pointer}: invalid SHA-256 digest {child!r}",
                failures,
            )


def json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "#":
        return document
    if not pointer.startswith("#/"):
        raise KeyError(pointer)
    current = document
    for token in pointer[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        else:
            current = current[token]
    return current


def validate_refs(path: Path, document: Any, failures: list[str]) -> None:
    for pointer, value in walk_values(document):
        if not isinstance(value, dict) or "$ref" not in value:
            continue
        ref = value["$ref"]
        if not isinstance(ref, str):
            fail(f"{path.relative_to(ROOT)} {pointer}: $ref must be a string", failures)
            continue
        if ref.startswith("#"):
            try:
                json_pointer(document, ref)
            except (KeyError, IndexError, ValueError):
                fail(f"{path.relative_to(ROOT)} {pointer}: unresolved local $ref {ref}", failures)
            continue
        target = ref.split("#", 1)[0]
        if target and not (path.parent / target).resolve().exists():
            fail(f"{path.relative_to(ROOT)} {pointer}: missing external $ref target {target}", failures)


def validate_schemas_and_examples(failures: list[str]) -> tuple[int, int]:
    schema_paths = sorted(SCHEMAS.glob("*.schema.json"))
    example_paths = sorted(EXAMPLES.glob("*.example.json"))
    if not schema_paths:
        fail("no JSON Schemas found", failures)
        return 0, 0

    schemas: dict[str, Any] = {}
    store: dict[str, Any] = {}
    for path in schema_paths:
        try:
            schema = load_json(path)
            Draft202012Validator.check_schema(schema)
        except Exception as error:
            fail(f"{path.relative_to(ROOT)}: invalid JSON Schema: {error}", failures)
            continue
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            fail(f"{path.relative_to(ROOT)}: missing stable $id", failures)
        schemas[path.name] = schema
        store[path.name] = schema
        store[path.resolve().as_uri()] = schema
        if isinstance(schema_id, str):
            store[schema_id] = schema
        validate_refs(path, schema, failures)

    expected_examples = {
        name.replace(".schema.json", ".example.json")
        for name in schemas
        if name != "common.schema.json"
    }
    actual_examples = {path.name for path in example_paths}
    for missing in sorted(expected_examples - actual_examples):
        fail(f"missing fixture for schema: contracts/examples/{missing}", failures)
    for orphan in sorted(actual_examples - expected_examples):
        fail(f"fixture has no matching schema: contracts/examples/{orphan}", failures)

    for path in example_paths:
        schema_name = path.name.replace(".example.json", ".schema.json")
        schema = schemas.get(schema_name)
        if schema is None:
            continue
        try:
            instance = load_json(path)
        except Exception as error:
            fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}", failures)
            continue
        validate_sha256_strings(path, instance, failures)
        resolver = RefResolver(
            base_uri=(SCHEMAS / schema_name).resolve().as_uri(),
            referrer=schema,
            store=store,
        )
        validator = Draft202012Validator(schema, resolver=resolver)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
            location = "$" + "".join(
                f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.path
            )
            fail(f"{path.relative_to(ROOT)} {location}: {error.message}", failures)

    return len(schema_paths), len(example_paths)


def validate_registries(failures: list[str]) -> int:
    paths = sorted(REGISTRIES.glob("*.json"))
    required = {
        "effect-kinds.json",
        "event-types.json",
        "error-categories.json",
        "hard-gates.json",
        "conformance-modules.json",
    }
    missing = required - {path.name for path in paths}
    for name in sorted(missing):
        fail(f"missing registry: contracts/registries/{name}", failures)

    registry_data: dict[str, Any] = {}
    for path in paths:
        try:
            data = load_json(path)
        except Exception as error:
            fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}", failures)
            continue
        registry_data[path.name] = data
        validate_sha256_strings(path, data, failures)
        if not isinstance(data, dict):
            fail(f"{path.relative_to(ROOT)}: registry root must be an object", failures)
            continue
        if not isinstance(data.get("registry"), str) or not isinstance(data.get("registryVersion"), str):
            fail(f"{path.relative_to(ROOT)}: missing registry and registryVersion", failures)
        entries = data.get("entries")
        if not isinstance(entries, list):
            fail(f"{path.relative_to(ROOT)}: entries must be an array", failures)
            continue
        ids: list[str] = []
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                fail(f"{path.relative_to(ROOT)} entries[{index}]: missing string id", failures)
                continue
            ids.append(entry["id"])
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        if duplicates:
            fail(f"{path.relative_to(ROOT)}: duplicate IDs {duplicates}", failures)

    for name in ("effect-kinds.json", "event-types.json"):
        data = registry_data.get(name)
        if isinstance(data, dict):
            for entry in data.get("entries", []):
                identifier = entry.get("id") if isinstance(entry, dict) else None
                if isinstance(identifier, str) and not EVENT_ID_RE.fullmatch(identifier):
                    fail(f"contracts/registries/{name}: invalid identifier {identifier!r}", failures)

    hard_gates = registry_data.get("hard-gates.json")
    if isinstance(hard_gates, dict):
        for entry in hard_gates.get("entries", []):
            identifier = entry.get("id") if isinstance(entry, dict) else None
            if isinstance(identifier, str) and not GATE_ID_RE.fullmatch(identifier):
                fail(f"contracts/registries/hard-gates.json: invalid gate ID {identifier!r}", failures)
        fixture_path = EXAMPLES / "hard-gate-registry.example.json"
        if fixture_path.exists():
            fixture = load_json(fixture_path)
            registry_ids = {entry["id"] for entry in hard_gates.get("entries", [])}
            fixture_ids = {entry["id"] for entry in fixture.get("entries", [])}
            if registry_ids != fixture_ids:
                fail("hard-gate registry fixture IDs differ from canonical registry", failures)

    return len(paths)


def validate_openapi(failures: list[str]) -> None:
    if not OPENAPI.exists():
        fail("missing contracts/openapi/ara-api-profile.yaml", failures)
        return
    try:
        document = load_yaml(OPENAPI)
    except Exception as error:
        fail(f"{OPENAPI.relative_to(ROOT)}: invalid YAML: {error}", failures)
        return
    validate_sha256_strings(OPENAPI, document, failures)
    if not isinstance(document, dict) or document.get("openapi") != "3.1.1":
        fail("OpenAPI profile must declare openapi: 3.1.1", failures)
        return
    paths = document.get("paths")
    if not isinstance(paths, dict) or not paths:
        fail("OpenAPI profile has no paths", failures)
    operation_ids: list[str] = []
    if isinstance(paths, dict):
        for path_item in paths.values():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                if method not in {"get", "put", "post", "delete", "patch", "head", "options", "trace"}:
                    continue
                if not isinstance(operation, dict) or not isinstance(operation.get("operationId"), str):
                    fail(f"OpenAPI operation {method} missing operationId", failures)
                else:
                    operation_ids.append(operation["operationId"])
    duplicates = sorted({item for item in operation_ids if operation_ids.count(item) > 1})
    if duplicates:
        fail(f"OpenAPI duplicate operationIds: {duplicates}", failures)
    for required in ("resumeRun", "evidenceReplay", "rerun", "decideApproval"):
        if required not in operation_ids:
            fail(f"OpenAPI profile missing operationId {required}", failures)
    validate_refs(OPENAPI, document, failures)


def validate_asyncapi(failures: list[str]) -> None:
    if not ASYNCAPI.exists():
        fail("missing contracts/asyncapi/ara-events-profile.yaml", failures)
        return
    try:
        document = load_yaml(ASYNCAPI)
    except Exception as error:
        fail(f"{ASYNCAPI.relative_to(ROOT)}: invalid YAML: {error}", failures)
        return
    validate_sha256_strings(ASYNCAPI, document, failures)
    if not isinstance(document, dict) or document.get("asyncapi") != "3.0.0":
        fail("AsyncAPI profile must declare asyncapi: 3.0.0", failures)
        return
    if not isinstance(document.get("channels"), dict) or not document["channels"]:
        fail("AsyncAPI profile has no channels", failures)
    if not isinstance(document.get("operations"), dict) or not document["operations"]:
        fail("AsyncAPI profile has no operations", failures)
    validate_refs(ASYNCAPI, document, failures)


def validate_document_fences(failures: list[str]) -> tuple[int, int]:
    json_count = 0
    yaml_count = 0
    for path in sorted(ROOT.rglob("*.mdx")):
        if ".git" in path.parts or "_drafts" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for index, body in enumerate(re.findall(r"```json\s*\n(.*?)\n```", text, flags=re.S), 1):
            json_count += 1
            try:
                document = json.loads(body)
            except Exception as error:
                fail(f"{path.relative_to(ROOT)}: invalid JSON fence {index}: {error}", failures)
                continue
            validate_sha256_strings(path, document, failures, context=f"JSON fence {index}")
        for index, body in enumerate(re.findall(r"```ya?ml\s*\n(.*?)\n```", text, flags=re.S), 1):
            yaml_count += 1
            try:
                document = yaml.safe_load(body)
            except Exception as error:
                fail(f"{path.relative_to(ROOT)}: invalid YAML fence {index}: {error}", failures)
                continue
            validate_sha256_strings(path, document, failures, context=f"YAML fence {index}")
    return json_count, yaml_count


def main() -> int:
    failures: list[str] = []

    schema_count, fixture_count = validate_schemas_and_examples(failures)
    registry_count = validate_registries(failures)
    validate_openapi(failures)
    validate_asyncapi(failures)
    json_fences, yaml_fences = validate_document_fences(failures)

    if failures:
        print("Contract validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(
        "Contract validation passed for "
        f"{schema_count} schemas, {fixture_count} fixtures, {registry_count} registries, "
        f"OpenAPI, AsyncAPI, {json_fences} JSON fences, and {yaml_fences} YAML fences."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
