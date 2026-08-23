#!/usr/bin/env python3
"""Constrói o exemplo de conjunto de transferência a partir dos pacotes existentes.

As unidades são cópias dos pacotes de exemplo já no repositório, e por isso não
são versionadas: duplicar dois pacotes completos em Git seria ruído, e os seus
bytes já estão sob revisão nos respectivos diretórios. O que é versionado é o que
este exemplo acrescenta — a declaração de transferência, o selo e a evidência de
custódia.

Reconstrói `unidades/` e recalcula `transferencia.json` a partir das unidades
reais, pelo que uma alteração a um pacote de exemplo se propaga sem edição manual
de digests.
"""

import argparse
import base64
import hashlib
import json
import shutil
import sys
from pathlib import Path

try:
    import rfc8785
except ImportError:
    print("ERRO: instale tools/requirements.txt para obter rfc8785", file=sys.stderr)
    raise SystemExit(1)


ROOT = Path(__file__).resolve().parent.parent
DESTINO = ROOT / "specs/ndf/examples/ndfxfer-example"

# Unidades do conjunto: pacote de origem → nome dentro de unidades/
UNIDADES = [
    (ROOT / "specs/ndf/examples/ndfpkg-example", "oficio-of-2026-00123.ndfpkg"),
    (ROOT / "specs/ndf/examples/captura-requerimento", "requerimento-eb-2026-4471.ndfpkg"),
]


def digest(dados: bytes) -> str:
    return "sha256:" + hashlib.sha256(dados).hexdigest()


def referencias_externas(cores: dict[str, dict]) -> list[dict]:
    """Relações das unidades cujo alvo não está no conjunto.

    Derivada, e é isso que a torna verificável: o recetor recomputa-a a partir do
    que recebeu e compara com o declarado (D-XFER-1).
    """
    presentes = set(cores)
    fora = []
    for ndf_id, core in sorted(cores.items()):
        for relacao in core.get("relacoes", []) or []:
            alvo = relacao.get("alvo", {})
            if alvo.get("ndf_id") in presentes:
                continue
            fora.append({
                "declarada_por": ndf_id,
                "tipo": relacao.get("tipo"),
                "alvo": {
                    "ndf_id": alvo.get("ndf_id"),
                    "payload_hash": alvo.get("payload_hash"),
                },
            })
    return fora


def build() -> None:
    unidades_dir = DESTINO / "unidades"
    if unidades_dir.exists():
        shutil.rmtree(unidades_dir)
    unidades_dir.mkdir(parents=True)

    unidades, cores = [], {}
    for origem, nome in UNIDADES:
        shutil.copytree(origem, unidades_dir / nome)
        core = json.loads((origem / "ndf-core.json").read_text(encoding="utf-8"))
        manifest = json.loads((origem / "manifest.json").read_text(encoding="utf-8"))
        cores[core["ndf_id"]] = core
        unidades.append({
            "ndf_id": core["ndf_id"],
            "payload_hash": manifest["payload_hash"],
            "validation_code": manifest["validation_code"],
            "ficheiro": f"unidades/{nome}",
        })

    declaracao_path = DESTINO / "transferencia.json"
    declaracao = json.loads(declaracao_path.read_text(encoding="utf-8"))
    declaracao["unidades"] = unidades
    declaracao["referencias_externas"] = referencias_externas(cores)

    # O inventário cobre os ficheiros próprios do contentor. As unidades ficam
    # de fora por decisão de desenho: são cobertas por unidades[].payload_hash,
    # que as prende ao conteúdo documental e não a uma materialização concreta.
    inventario = []
    for ficheiro in sorted(DESTINO.rglob("*")):
        if not ficheiro.is_file():
            continue
        rel = ficheiro.relative_to(DESTINO).as_posix()
        if rel.startswith("unidades/") or rel in ("transferencia.json",
                                                  "transferencia-envelope.json",
                                                  "README.md"):
            continue
        inventario.append({"ficheiro": rel, "hash_sha256": digest(ficheiro.read_bytes())})
    declaracao["inventario"] = inventario

    bytes_canonicos = rfc8785.dumps(declaracao)
    declaracao_path.write_bytes(bytes_canonicos)

    payload_hash = digest(bytes_canonicos)
    bruto = hashlib.sha256(
        f"{declaracao['transferencia_id']}|{payload_hash}".encode("utf-8")).digest()
    codigo = "NDF-" + base64.b32encode(bruto).decode("ascii").rstrip("=")[:20]

    envelope_path = DESTINO / "transferencia-envelope.json"
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    envelope["payload_hash"] = payload_hash
    envelope["validation_code"] = codigo
    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")

    print(f"{DESTINO.name}: {len(unidades)} unidades, "
          f"{len(declaracao['referencias_externas'])} referências externas, "
          f"payload_hash={payload_hash}")


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
