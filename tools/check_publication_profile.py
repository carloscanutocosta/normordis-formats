#!/usr/bin/env python3
"""Verifica gates editoriais mínimos dos drafts de publicação."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPECS = {
    "NDF": ROOT / "specs/ndf/SPEC.md",
    "NDT": ROOT / "specs/ndt/SPEC.md",
    "NCRTF": ROOT / "specs/ncrtf/SPEC.md",
}
# Estados editoriais admissíveis, alinhados com os níveis de NORMALIZATION.md.
# "Revisão pública" (nível 2) só é declarável enquanto existir um período de
# revisão efetivamente aberto em docs/normalization/REVIEW-LOG.md.
ALLOWED_STATES = (
    "Draft — revisão pública por abrir",
    "Draft — Revisão pública",
)
REQUIRED = (
    r"Objetivo",
    r"Referências normativas",
    r"Termos e definições|Terminologia normativa",
    r"Conformidade",
    r"Anexo A \(informativo\)",
)
FORBIDDEN_HEADINGS = re.compile(
    r"^#{2,4}\s+.*(?:Roadmap|Estimativas|Mapeamento jurídico|Armazenamento em base de dados \(informativo\))",
    re.I | re.M,
)


def main() -> int:
    failures = []
    for name, path in SPECS.items():
        text = path.read_text(encoding="utf-8")
        if not any(state in text for state in ALLOWED_STATES):
            allowed = " | ".join(ALLOWED_STATES)
            failures.append(f"{name}: estado editorial ausente ou não admissível ({allowed})")
        for pattern in REQUIRED:
            if not re.search(pattern, text, re.I):
                failures.append(f"{name}: elemento ausente /{pattern}/")
        forbidden = FORBIDDEN_HEADINGS.search(text)
        if forbidden:
            failures.append(f"{name}: material informativo no corpo — {forbidden.group(0)}")
        if text.index("Conformidade") > text.index("Anexo A (informativo)"):
            failures.append(f"{name}: conformidade deve preceder anexos informativos")
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1
    print(f"PASS publication profile: {len(SPECS)} drafts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
