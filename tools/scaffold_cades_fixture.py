#!/usr/bin/env python3
"""Cria o esqueleto de uma fixture CAdES B-LTA.

O script prepara a estrutura, copia os modelos de manifesto e de expected.json
e cria um README local para o caso. Não cria artefactos criptográficos reais.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "conformance/cades"
MANIFEST_TEMPLATE = BASE / "manifests/manifest.template.json"
EXPECTED_TEMPLATE = BASE / "expected/expected.template.json"

POSITIVES = {
    "advanced-real": {
        "case_kind": "positive",
        "signature_kind": "sea",
    },
    "qualified-real": {
        "case_kind": "positive",
        "signature_kind": "seq",
    },
    "institutional-seal-real": {
        "case_kind": "positive",
        "signature_kind": "institutional_seal",
    },
    "expired-certificate-historical": {
        "case_kind": "positive",
        "signature_kind": "sea",
    },
    "offline-tsa-real": {
        "case_kind": "positive",
        "signature_kind": "sea",
    },
}

NEGATIVES = {
    "payload-tampered": "advanced-real",
    "signature-tampered": "advanced-real",
    "timestamp-missing": "advanced-real",
    "timestamp-altered": "advanced-real",
    "revocation-before-signing": "qualified-real",
    "chain-untrusted": "institutional-seal-real",
    "payload-hash-mismatch": "offline-tsa-real",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def scaffold_case(case_id: str, case_kind: str, signature_kind: str, parent_case: str | None = None) -> Path:
    category = "valid" if case_kind == "positive" else "negative"
    case_dir = BASE / category / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("certificates", "revocation", "timestamps", "trust"):
        (case_dir / sub).mkdir(parents=True, exist_ok=True)

    manifest = load_json(MANIFEST_TEMPLATE)
    manifest.update({
        "case_id": f"{category}/{case_id}",
        "case_kind": case_kind,
        "signature_kind": signature_kind,
        "fixture_state": "skeleton",
    })
    manifest["source"]["issuer"] = "TO-DO"
    manifest["source"]["environment"] = "laboratorio-controlado"
    manifest["source"]["generated_at"] = "2026-01-01T00:00:00Z"
    manifest["trust"]["anchor_set"] = "trust/anchor.pem"
    manifest["trust"]["policy"] = "skeleton"
    if parent_case:
        manifest["parent_case"] = f"valid/{parent_case}"
    dump_json(case_dir / "manifest.json", manifest)

    expected = load_json(EXPECTED_TEMPLATE)
    expected.update({
        "case_id": f"{category}/{case_id}",
        "decision": "accept" if case_kind == "positive" else "reject",
        "signature_kind": signature_kind,
        "fixture_state": "skeleton",
    })
    if parent_case:
        expected["mutation_of"] = f"valid/{parent_case}"
    expected["notes"] = [
        "Esqueleto gerado automaticamente.",
        "Substituir os placeholders por prova criptográfica real antes de publicar.",
    ]
    dump_json(case_dir / "expected.json", expected)

    readme = case_dir / "README.md"
    readme.write_text(
        f"""# {category}/{case_id}

Esqueleto de fixture CAdES B-LTA.

## Estado

Este diretório foi preparado por `tools/scaffold_cades_fixture.py` e ainda não
contém artefactos criptográficos reais.

## Próximos passos

- adicionar `payload.jcs`;
- adicionar `payload.sha256`;
- adicionar `signature.p7s`;
- preencher `certificates/`, `revocation/`, `timestamps/` e `trust/`;
- substituir o `fixture_state` para indicar material real;
- validar com `tools/check_cades_gate.py`.
""",
        encoding="utf-8",
    )

    return case_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="cria o esqueleto de todas as fixtures previstas")
    parser.add_argument("--case-id", help="identificador curto do caso, sem o prefixo valid/negative")
    parser.add_argument("--case-kind", choices=("positive", "negative"), help="tipo do caso")
    parser.add_argument("--signature-kind", help="tipo de assinatura CAdES esperado")
    parser.add_argument("--parent-case", help="caso positivo de origem para a mutação negativa")
    args = parser.parse_args()

    if args.all:
        for case_id, meta in POSITIVES.items():
            scaffold_case(case_id, meta["case_kind"], meta["signature_kind"])
        for case_id, parent in NEGATIVES.items():
            scaffold_case(case_id, "negative", "sea", parent_case=parent)
        print("PASS cades scaffold: todas as fixtures esqueleto criadas")
        return 0

    if not args.case_id or not args.case_kind or not args.signature_kind:
        parser.error("--case-id, --case-kind e --signature-kind são obrigatórios sem --all")

    scaffold_case(args.case_id, args.case_kind, args.signature_kind, parent_case=args.parent_case)
    print(f"PASS cades scaffold: {args.case_kind}/{args.case_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
