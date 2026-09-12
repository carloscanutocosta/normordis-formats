#!/usr/bin/env python3
"""Confirma que tools/validate.py falha a arrancar sem rfc8785 (R17).

Antes desta correção, rfc8785 era a única dependência opcional do projeto:
`tools/validate.py` importava-a em `try/except` e, na sua ausência,
omitia silenciosamente a verificação de bytes canónicos JCS em
`validate_package_dir` — um pacote não-canónico podia obter `PASS` sem que
o resultado o assinalasse. Reproduzido na avaliação de 2026-09-11 simulando
a ausência da biblioteca.

Este teste simula exatamente essa ausência, num subprocesso isolado (para
não interferir com o `sys.modules` deste processo), e confirma que
`validate.py` recusa arrancar — não que produza um resultado incompleto.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SETUP = (
    "import sys; sys.modules['rfc8785'] = None; "
    "sys.argv = ['validate.py']; "
    "import runpy; runpy.run_path('tools/validate.py', run_name='__main__')"
)


def main() -> int:
    proc = subprocess.run(
        [sys.executable, "-c", SETUP],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    falhas = []
    if proc.returncode == 0:
        falhas.append(
            f"validate.py terminou com sucesso (código 0) sem rfc8785 — "
            f"devia recusar arrancar"
        )
    if "ERRO: instale tools/requirements.txt para obter rfc8785" not in proc.stderr:
        falhas.append(
            "mensagem de erro esperada não apareceu em stderr: "
            f"{proc.stderr.strip()!r}"
        )
    if "PASS" in proc.stdout:
        falhas.append(
            f"stdout contém 'PASS' apesar da falha de arranque — "
            f"resultado incompleto a passar por completo: {proc.stdout.strip()!r}"
        )

    if falhas:
        for f in falhas:
            print(f"FAIL {f}")
        return 1
    print("PASS jcs required: validate.py recusa arrancar sem rfc8785")
    return 0


if __name__ == "__main__":
    sys.exit(main())
