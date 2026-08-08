#!/usr/bin/env python3
"""Gera o índice de casos de conformidade a partir dos ficheiros reais.

Substitui a manutenção manual de tabelas no README, que se desatualizava
sempre que se acrescentavam casos (revisão pré-RC, achado F15).
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "conformance/INDEX.md"
SUITES = ("ndf", "ncrtf", "ndt", "custody", "jcs")


def describe(path: Path) -> str:
    """Extrai a descrição do caso a partir dos campos _comment/_expected_error."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return "—"
    if not isinstance(data, dict):
        return "—"
    text = data.get("_comment") or data.get("_expected_error") or "—"
    text = " ".join(str(text).split())
    return text[:160] + ("…" if len(text) > 160 else "")


def main() -> int:
    lines = [
        "# Índice de casos de conformidade",
        "",
        "Este ficheiro é gerado por `tools/build_conformance_index.py`. Não deve ser",
        "editado manualmente. A definição normativa de conformidade está em",
        "`specs/ndf/SPEC.md` §9.",
        "",
    ]
    total = 0
    for suite in SUITES:
        base = ROOT / "conformance" / suite
        if not base.is_dir():
            continue
        lines.append(f"## {suite.upper()}")
        lines.append("")
        for bucket in ("valid", "invalid"):
            folder = base / bucket
            if not folder.is_dir():
                continue
            files = sorted(folder.glob("*.json"))
            if not files:
                continue
            rotulo = "devem ser aceites" if bucket == "valid" else "devem ser rejeitados"
            lines.append(f"### `{bucket}/` — {rotulo} ({len(files)})")
            lines.append("")
            lines.append("| Ficheiro | Descrição |")
            lines.append("|---|---|")
            for f in files:
                lines.append(f"| `{suite}/{bucket}/{f.name}` | {describe(f)} |")
                total += 1
            lines.append("")
        # ficheiros soltos (ex.: conformance/custody/*.json)
        loose = sorted(p for p in base.glob("*.json"))
        if loose:
            lines.append(f"### vetores diretos ({len(loose)})")
            lines.append("")
            lines.append("| Ficheiro | Descrição |")
            lines.append("|---|---|")
            for f in loose:
                lines.append(f"| `{suite}/{f.name}` | {describe(f)} |")
                total += 1
            lines.append("")

    lines.append(f"**Total: {total} casos.**")
    lines.append("")
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"PASS conformance index: {total} casos inventariados em {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
