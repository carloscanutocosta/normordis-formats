#!/usr/bin/env python3
"""Gera e valida o índice de requisitos normativos NORMORDIS."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs/normalization/REQUIREMENTS.md"
SOURCES = (
    ROOT / "specs/ndf/SPEC.md",
    ROOT / "specs/ncrtf/SPEC.md",
    ROOT / "specs/ndt/RENDERER-CONFORMANCE.md",
)
ID_RE = re.compile(
    r"\*\*((?:NDF-(?:PROD|READ|PKG)|NCRTF-(?:PROD|READ)|NDT-RENDER|CUST-REQ)-\d{3})"
)


def evidence(requirement_id: str) -> str:
    if requirement_id.startswith("NDF-PROD"):
        return "schema NDF + `conformance/ndf/valid/` + verificações semânticas"
    if requirement_id.startswith("NDF-READ"):
        return "`conformance/ndf/valid/` e `conformance/ndf/invalid/`"
    if requirement_id.startswith("NDF-PKG"):
        return "verificador de pacote + exemplo `.ndfpkg`"
    if requirement_id.startswith("NCRTF-PROD"):
        return "schema NCRTF + vetores válidos + regras R1–R6"
    if requirement_id.startswith("NCRTF-READ"):
        return "vetores NCRTF válidos e inválidos"
    if requirement_id.startswith("CUST-REQ"):
        return "schema custody-event + `tools/check_custody.py` + `conformance/custody/` — Perfil de Ciclo de Vida NORMORDIS, opcional (não requisito de conformidade NDF)"
    return "suite NDT; resultados de referência pendentes quando aplicável"


def main() -> int:
    rows: list[tuple[str, str, int, str]] = []
    seen: dict[str, tuple[Path, int]] = {}
    for source in SOURCES:
        for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            match = ID_RE.search(line)
            if not match:
                continue
            requirement_id = match.group(1)
            if requirement_id in seen:
                previous = seen[requirement_id]
                raise SystemExit(
                    f"ID duplicado {requirement_id}: {previous[0]}:{previous[1]} e "
                    f"{source}:{line_number}"
                )
            seen[requirement_id] = (source, line_number)
            summary = re.sub(r"[*`]", "", line.strip())
            summary = re.sub(r"^\d+\.\s*", "", summary)
            rows.append((requirement_id, source.relative_to(ROOT).as_posix(), line_number, summary))

    rows.sort()
    text = [
        "# Índice de requisitos normativos",
        "",
        "Este ficheiro é gerado por `tools/build_requirements_index.py`. Não deve ser",
        "editado manualmente. A cláusula de origem permanece normativa; esta tabela é",
        "um índice de rastreabilidade.",
        "",
        "| ID | Origem | Resumo | Evidência atual |",
        "|---|---|---|---|",
    ]
    for requirement_id, source, line_number, summary in rows:
        text.append(
            f"| `{requirement_id}` | `{source}:{line_number}` | {summary} | "
            f"{evidence(requirement_id)} |"
        )
    text.extend(("", f"Total: **{len(rows)} requisitos identificados**.", ""))
    OUTPUT.write_text("\n".join(text), encoding="utf-8")
    print(f"PASS requirements: {len(rows)} IDs únicos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
