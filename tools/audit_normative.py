#!/usr/bin/env python3
"""Audita linguagem modal, IDs e cobertura das cláusulas normativas."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs/normalization/NORMATIVE-STATEMENTS.md"
SOURCES = {
    ROOT / "specs/ndf/SPEC.md": "NDF",
    ROOT / "specs/ncrtf/SPEC.md": "NCRTF",
    ROOT / "specs/ndt/SPEC.md": "NDT",
    ROOT / "specs/ndt/RENDERER-CONFORMANCE.md": "NDT-RENDER",
}
MODAL = re.compile(r"\b(NÃO DEVEM|NÃO DEVE|DEVEM|DEVE|PODEM|PODE|RECOMENDA-SE|NÃO RECOMENDADO|RECOMENDADO)\b")
ID_PATTERN = (
    r"(?:NDF-(?:PROD|READ|PKG)|NCRTF-(?:PROD|READ)"
    r"|NDT-(?:PROD|RENDER)|CUST-REQ)-\d{3}"
)
ID_RE = re.compile(rf"\b({ID_PATTERN})\b")
# Só a definição do requisito conta como origem: é marcada a negrito, tal como
# em `tools/build_requirements_index.py`. Uma menção em prosa ou numa tabela de
# agrupamento é referência cruzada, não redefinição.
DEF_RE = re.compile(rf"\*\*({ID_PATTERN})")
ENGLISH_MODAL = re.compile(r"\b(MUST|SHALL|SHOULD|MAY)(?: NOT)?\b")
LOWER_MODAL = re.compile(r"\b(não devem|não deve|devem|deve|podem|pode|recomenda-se)\b", re.I)
LOWER_ALLOWED = (
    re.compile(r"não pode violar", re.I),
    re.compile(r"pode incluir ou omitir", re.I),
    re.compile(r"pode estar ausente", re.I),
    re.compile(r"pode ter múltiplas versões", re.I),
    re.compile(r"podem ter limites", re.I),
    re.compile(r"pode ser comprometido", re.I),
    re.compile(r"podem tornar-se obsoletos", re.I),
)


def coverage(document: str, section: str) -> str:
    if document == "NDF-RENDER":
        return "NDT-RENDER-*"
    major = section.split(".", 1)[0]
    if document == "NDF":
        return {
            "1": "NDF-PROD-001..011",
            "2": "NDF-PROD-001,006,008,009; NDF-READ-001..005",
            "3": "NDF-PROD-006,007",
            "4": "NDF-PROD-005; NDF-READ-006..008",
            "5": "NDF-PROD-005",
            "6": "NDF-PROD-010",
            "7": "NDF-READ-002,003",
            "8": "NDF-PKG-001..006",
            "9": "requisito identificado na própria cláusula",
        }.get(major, "avaliação editorial")
    if document == "NCRTF":
        return "NCRTF-PROD-001..007; NCRTF-READ-001..005"
    if document == "NDT":
        return {
            "1": "NDT-PROD-003; NDT-RENDER-005,007",
            "2": "NDT-PROD-002",
            "3": "NDT-RENDER-011",
            "4": "NDT-PROD-004,005,006; NDT-RENDER-002,007",
            "5": "NDT-PROD-007..019; NDT-RENDER-008..011",
            "6": "NDT-PROD-001",
            "7": "NDT-PROD-003; NDT-RENDER-001",
            "8": "NDT-PROD-017..019; NDT-RENDER-005",
            "9": "requisito identificado na própria cláusula",
        }.get(major, "avaliação editorial")
    return "NDT-RENDER-001..011"


def main() -> int:
    rows = []
    ids: dict[str, str] = {}
    failures = []
    for path, document in SOURCES.items():
        section = "preâmbulo"
        in_code = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("```"):
                in_code = not in_code
                continue
            heading = re.match(r"^#{2,4}\s+(?:Anexo\s+\w+|([0-9]+(?:\.[0-9]+)*))", line)
            if heading:
                section = heading.group(1) or "anexo"
            if in_code:
                continue
            for found in DEF_RE.findall(line):
                if found in ids:
                    failures.append(f"ID duplicado {found}: {ids[found]} e {path}:{number}")
                ids[found] = f"{path.relative_to(ROOT)}:{number}"
            if ENGLISH_MODAL.search(line):
                failures.append(f"modal inglês em {path.relative_to(ROOT)}:{number}")
            lower = LOWER_MODAL.search(line)
            if lower and lower.group(0) == lower.group(0).lower():
                if not any(pattern.search(line) for pattern in LOWER_ALLOWED):
                    failures.append(f"modal minúsculo ambíguo em {path.relative_to(ROOT)}:{number}: {line.strip()}")
            if not MODAL.search(line):
                continue
            explicit = DEF_RE.search(line)
            kind = "principal" if explicit else ("definição" if section in {"1.0", "2"} and "Term" in line else "subordinado")
            rows.append((document, section, path.relative_to(ROOT).as_posix(), number, kind, explicit.group(1) if explicit else coverage(document, section), line.strip()))

    text = [
        "# Inventário de declarações normativas",
        "",
        "Gerado por `tools/audit_normative.py`. As declarações subordinadas são",
        "cobertas pelas famílias de conformidade indicadas; os IDs principais",
        "permanecem definidos no texto normativo.",
        "",
        "| Documento | Cláusula | Origem | Tipo | Cobertura | Declaração |",
        "|---|---:|---|---|---|---|",
    ]
    for document, section, source, number, kind, mapped, line in rows:
        clean = line.replace("|", "\\|")
        text.append(f"| {document} | {section} | `{source}:{number}` | {kind} | `{mapped}` | {clean} |")
    text.extend(("", f"Total: **{len(rows)} declarações com modalidade normativa**.", ""))
    OUTPUT.write_text("\n".join(text), encoding="utf-8")
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1
    print(f"PASS normative audit: {len(ids)} IDs; {len(rows)} declarações inventariadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
