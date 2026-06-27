#!/usr/bin/env python3
"""Audita a estrutura operacional do gate CAdES B-LTA.

Este verificador não exige ainda fixtures reais. Ele confirma que o plano,
as pastas esperadas e os artefactos mínimos estão documentados, e produz um
relatório explícito do que está concluído e do que continua pendente.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "docs/normalization/CADES-GATE-PLAN.md"
README = ROOT / "conformance/cades/README.md"
BASE = ROOT / "conformance/cades"
MANIFESTS = BASE / "manifests"
EXPECTED = BASE / "expected"

EXPECTED_TOP_LEVEL = (
    "valid",
    "negative",
    "manifests",
    "reports",
    "trust",
)

EXPECTED_POSITIVE_CASES = (
    "valid/advanced-real",
    "valid/qualified-real",
    "valid/institutional-seal-real",
    "valid/expired-certificate-historical",
    "valid/offline-tsa-real",
)

EXPECTED_NEGATIVE_CASES = (
    "negative/payload-tampered",
    "negative/signature-tampered",
    "negative/timestamp-missing",
    "negative/timestamp-altered",
    "negative/revocation-before-signing",
    "negative/chain-untrusted",
    "negative/payload-hash-mismatch",
)

REQUIRED_ARTIFACTS = (
    "payload.jcs",
    "payload.sha256",
    "signature.p7s",
    "certificates",
    "revocation",
    "timestamps",
    "expected.json",
    "trust",
    "manifest.json",
)


@dataclass
class CaseStatus:
    case: str
    present: bool
    missing: list[str]


def file_contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def inspect_case(case_dir: Path) -> CaseStatus:
    missing: list[str] = []
    if not case_dir.exists():
        return CaseStatus(case=case_dir.as_posix(), present=False, missing=[*REQUIRED_ARTIFACTS])
    manifest = load_json(case_dir / "manifest.json") or {}
    expected = load_json(case_dir / "expected.json") or {}
    if manifest.get("fixture_state") == "skeleton" or expected.get("fixture_state") == "skeleton":
        missing.append("fixture_state=skeleton")
    for item in REQUIRED_ARTIFACTS:
        target = case_dir / item
        if not target.exists():
            missing.append(item)
    return CaseStatus(case=case_dir.as_posix(), present=not missing, missing=missing)


def main() -> int:
    failures: list[str] = []
    pending: list[str] = []

    if not PLAN.is_file():
        failures.append("plano ausente: docs/normalization/CADES-GATE-PLAN.md")
    else:
        if not file_contains(PLAN, "Checklist executável"):
            failures.append("plano sem secção 'Checklist executável'")
        if not file_contains(PLAN, "Casos positivos"):
            failures.append("plano sem secção de casos positivos")
        if not file_contains(PLAN, "Casos negativos"):
            failures.append("plano sem secção de casos negativos")

    if not README.is_file():
        failures.append("README de conformance ausente: conformance/cades/README.md")
    elif not file_contains(README, "Plano para fechar o gate"):
        failures.append("README de conformance sem referência ao plano")

    if not BASE.exists():
        pending.append("diretório base conformance/cades ainda não existe")
    else:
        for sub in EXPECTED_TOP_LEVEL:
            if not (BASE / sub).exists():
                pending.append(f"subdiretório em falta: conformance/cades/{sub}")

        for rel in EXPECTED_POSITIVE_CASES:
            status = inspect_case(BASE / rel)
            if not status.present:
                pending.append(f"caso positivo pendente: {rel} ({', '.join(status.missing)})")
        for rel in EXPECTED_NEGATIVE_CASES:
            status = inspect_case(BASE / rel)
            if not status.present:
                pending.append(f"caso negativo pendente: {rel} ({', '.join(status.missing)})")

    if MANIFESTS.exists():
        for required in ("README.md", "manifest.template.json", "manifest.example.json"):
            if not (MANIFESTS / required).is_file():
                pending.append(f"manifesto em falta: manifests/{required}")
    else:
        pending.append("diretório de manifestos em falta: conformance/cades/manifests")

    if EXPECTED.exists():
        for required in ("README.md", "expected.template.json", "expected.example.json"):
            if not (EXPECTED / required).is_file():
                pending.append(f"expectativa em falta: expected/{required}")
    else:
        pending.append("diretório de expectativas em falta: conformance/cades/expected")

    if failures:
        print("\n".join(f"FAIL {msg}" for msg in failures))
        return 1

    report = {
        "plan": str(PLAN.relative_to(ROOT)),
        "conformance_readme": str(README.relative_to(ROOT)),
        "manifests_readme": str((MANIFESTS / "README.md").relative_to(ROOT)) if MANIFESTS.exists() else None,
        "expected_readme": str((EXPECTED / "README.md").relative_to(ROOT)) if EXPECTED.exists() else None,
        "expected_positive_cases": len(EXPECTED_POSITIVE_CASES),
        "expected_negative_cases": len(EXPECTED_NEGATIVE_CASES),
        "pending": pending,
    }

    print(f"PASS cades gate plan: {PLAN.name}")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
