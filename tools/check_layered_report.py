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

Mais dois casos de robustez do próprio relatório, encontrados por revisão
adversarial ao commit 65a21e3: `--json` misturava mensagens humanas com o
JSON em stdout, e um `ndf-core.json` que não fosse objeto (ex.: `[]`)
derrubava o processo com `AttributeError` em vez de devolver um relatório.
"""

import hashlib
import json
import shutil
import subprocess
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
    camada1 = r1["camadas"]["assinatura_confianca"]
    if not r1["ok"]:
        falhas.append(f"ndfpkg-example devia passar estruturalmente: {r1}")
    if camada1["estado"] != "indeterminada" or "placeholder" not in (camada1["motivo"] or ""):
        falhas.append(f"esperado estado 'indeterminada' com placeholder no motivo, obtido: {camada1!r}")
    if camada1["estado"] == "aprovada":
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
        camada2 = r2["camadas"]["assinatura_confianca"]
        if camada2["estado"] != "indeterminada":
            falhas.append(f"esperado estado 'indeterminada' sem placeholder, obtido: {camada2!r}")
        if "placeholder" in (camada2["motivo"] or ""):
            falhas.append(f"marcador de placeholder não devia constar no motivo depois de removido: {camada2!r}")

    # 3. nivel_assinatura: nenhuma, sem selo.
    r3 = validate_package_report(ROOT / "specs/ndf/examples/captura-requerimento")
    camada3 = r3["camadas"]["assinatura_confianca"]
    if not r3["ok"]:
        falhas.append(f"captura-requerimento devia passar estruturalmente: {r3}")
    if camada3["estado"] != "não_executada":
        falhas.append(f"esperado estado 'não_executada' sem assinatura nem selo, obtido: {camada3!r}")

    # Metadados obrigatórios (R18): versão, perfil, política de confiança, instante.
    for chave in ("versao_verificador", "perfil_avaliacao", "instante_verificacao", "politica_confianca"):
        if chave not in r1:
            falhas.append(f"relatório sem metadado obrigatório: {chave}")

    # 4. --json produz JSON puro em stdout (revisão de 2026-09-12): mensagens
    # de leitura humana tinham de ir para stderr, não misturadas em stdout.
    proc = subprocess.run(
        [sys.executable, "tools/validate.py", "--package",
         "specs/ndf/examples/ndfpkg-example", "--json"],
        cwd=ROOT, capture_output=True, text=True,
    )
    try:
        json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        falhas.append(f"--json não produziu JSON puro em stdout: {e} — stdout: {proc.stdout[:200]!r}")

    # 5. ndf-core.json que não seja objeto não pode derrubar o processo com
    # exceção não tratada — tem de devolver relatório com estrutura reprovada
    # e as restantes camadas 'não_executada' (revisão de 2026-09-12).
    with tempfile.TemporaryDirectory(prefix="normordis-layered-") as tmp:
        target = Path(tmp) / "core-nao-objeto"
        shutil.copytree(ROOT / "specs/ndf/examples/ndfpkg-example", target)
        (target / "ndf-core.json").write_text("[]", encoding="utf-8")
        try:
            r5 = validate_package_report(target, json_mode=True)
        except Exception as e:  # noqa: BLE001 — é exatamente o que não deve acontecer
            falhas.append(f"ndf-core.json == '[]' derrubou o validador: {type(e).__name__}: {e}")
        else:
            if r5["ok"]:
                falhas.append("ndf-core.json == '[]' devia reprovar, não passar")
            if r5["camadas"]["estrutura"]["estado"] != "reprovada":
                falhas.append(f"estrutura devia estar 'reprovada': {r5['camadas']['estrutura']}")
            for nome in ("canonicalizacao", "integridade_componentes", "dependencias_interpretacao"):
                if r5["camadas"][nome]["estado"] != "não_executada":
                    falhas.append(f"{nome} devia estar 'não_executada' quando a estrutura impede a verificação: {r5['camadas'][nome]}")

    if falhas:
        for f in falhas:
            print(f"FAIL {f}")
        print(f"FAIL layered report: {len(falhas)} problemas")
        return 1
    print("PASS layered report: 3 estados de assinatura_confianca + metadados + robustez de --json e estrutura inválida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
