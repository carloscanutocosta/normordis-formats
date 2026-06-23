#!/usr/bin/env python3
"""Valida identidade e cobertura estrutural do corpus semântico NDT."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "conformance/ndt/semantic/corpus.json"


def node_types(value):
    found = set()
    if isinstance(value, dict):
        if isinstance(value.get("tipo"), str):
            found.add(value["tipo"])
        for child in value.values():
            found.update(node_types(child))
    elif isinstance(value, list):
        for child in value:
            found.update(node_types(child))
    return found


def main() -> int:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    seen = set()
    failures = []
    for case in corpus["cases"]:
        case_id = case["id"]
        if case_id in seen:
            failures.append(f"{case_id}: ID duplicado")
        seen.add(case_id)
        path = ROOT / case["input"]
        if not path.is_file():
            failures.append(f"{case_id}: input ausente {case['input']}")
            continue
        ndt = json.loads(path.read_text(encoding="utf-8"))
        if ndt.get("schema_id") != case["expected_schema_id"]:
            failures.append(f"{case_id}: schema_id divergente")
        if len(ndt.get("paginas_def", [])) != case["expected_pages"]:
            failures.append(f"{case_id}: número de páginas divergente")
        missing = set(case["required_node_types"]) - node_types(ndt)
        if missing:
            failures.append(f"{case_id}: tipos ausentes {sorted(missing)}")
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1
    print(f"PASS NDT semantic corpus: {len(seen)} casos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
