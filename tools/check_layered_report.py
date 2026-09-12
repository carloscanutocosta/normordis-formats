#!/usr/bin/env python3
"""Confirma o relatório por camada de validate_package_report (R18).

Três estados possíveis da camada 'assinatura_confianca', cada um exercitado
contra um caso real, não hipotético:

1. Placeholder presente (ndfpkg-example, tal como está no repositório) →
   'indeterminada', com o marcador de placeholder assinalado.
2. Placeholder removido (cópia com material fictício mas sem o marcador de
   texto) → continua 'indeterminada' — este verificador nunca conclui
   'aprovada' para esta camada, com ou sem placeholder, porque não faz
   validação criptográfica — mas deixa de mencionar placeholder.
3. `nivel_assinatura: "nenhuma"` sem selo institucional
   (captura-requerimento, tal como está) → 'não_executada'.

Garante também que um `PASS` global nunca aparece sozinho quando a camada
'assinatura_confianca' não passou de 'indeterminada' — a saída legível tem
de imprimir essa camada à parte, sempre.
"""

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import validate_package_report  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    falhas = []

    # 1. Placeholder presente.
    r1 = validate_package_report(ROOT / "specs/ndf/examples/ndfpkg-example")
    estado1 = r1["camadas"]["assinatura_confianca"]["estado"]
    if not r1["ok"]:
        falhas.append(f"ndfpkg-example devia passar estruturalmente: {r1}")
    if "indeterminada" not in estado1 or "placeholder" not in estado1:
        falhas.append(f"esperado 'indeterminada' com placeholder, obtido: {estado1!r}")
    if "aprovada" in estado1:
        falhas.append("assinatura_confianca nunca deve reportar 'aprovada' — sem verificação criptográfica")

    # 2. Placeholder removido (material ainda fictício, mas sem o marcador).
    with tempfile.TemporaryDirectory(prefix="normordis-layered-") as tmp:
        target = Path(tmp) / "sem-placeholder"
        shutil.copytree(ROOT / "specs/ndf/examples/ndfpkg-example", target)
        envelope_path = target / "envelope.json"
        texto = envelope_path.read_text(encoding="utf-8")
        texto = texto.replace("PLACEHOLDER", "MATERIAL-FICTICIO-DE-TESTE")
        envelope_path.write_text(texto, encoding="utf-8")
        manifest_path = target / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        digest = "sha256:" + hashlib.sha256(envelope_path.read_bytes()).hexdigest()
        for item in manifest["inventario"]:
            if item["ficheiro"] == "envelope.json":
                item["hash_sha256"] = digest
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        r2 = validate_package_report(target)
        if not r2["ok"]:
            falhas.append(f"cópia sem placeholder devia passar estruturalmente: {r2['camadas']}")
        estado2 = r2["camadas"]["assinatura_confianca"]["estado"]
        if "indeterminada" not in estado2:
            falhas.append(f"esperado 'indeterminada' sem placeholder, obtido: {estado2!r}")
        if "placeholder" in estado2:
            falhas.append(f"marcador de placeholder não devia constar depois de removido: {estado2!r}")

    # 3. nivel_assinatura: nenhuma, sem selo.
    r3 = validate_package_report(ROOT / "specs/ndf/examples/captura-requerimento")
    estado3 = r3["camadas"]["assinatura_confianca"]["estado"]
    if not r3["ok"]:
        falhas.append(f"captura-requerimento devia passar estruturalmente: {r3}")
    if "não_executada" not in estado3:
        falhas.append(f"esperado 'não_executada' sem assinatura nem selo, obtido: {estado3!r}")

    # Metadados obrigatórios (R18): versão, perfil, política de confiança, instante.
    for chave in ("versao_verificador", "perfil_avaliacao", "instante_verificacao", "politica_confianca"):
        if chave not in r1:
            falhas.append(f"relatório sem metadado obrigatório: {chave}")

    if falhas:
        for f in falhas:
            print(f"FAIL {f}")
        print(f"FAIL layered report: {len(falhas)} problemas")
        return 1
    print("PASS layered report: 3 estados de assinatura_confianca + metadados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
