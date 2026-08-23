#!/usr/bin/env python3
"""Recalcula payload_hash, validation_code e inventário de um pacote de exemplo.

Ferramenta de manutenção do repositório, não normativa: existe para que uma
alteração ao NDF-core ou aos schemas embebidos num exemplo não obrigue a
recalcular digests à mão. Não assina nada — os exemplos com assinaturas reais
são selados pelo respectivo scaffolder de CAdES.
"""

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

try:
    import rfc8785
except ImportError:
    print("ERRO: instale tools/requirements.txt para obter rfc8785", file=sys.stderr)
    raise SystemExit(1)


def digest(dados: bytes) -> str:
    return "sha256:" + hashlib.sha256(dados).hexdigest()


def reseal(root: Path) -> None:
    core_path = root / "ndf-core.json"
    core = json.loads(core_path.read_text(encoding="utf-8"))

    # O NDF-core tem de conter exactamente os bytes JCS: reescreve-se sempre,
    # para que uma edição manual do exemplo não deixe bytes não canónicos.
    core_bytes = rfc8785.dumps(core)
    core_path.write_bytes(core_bytes)

    payload_hash = digest(core_bytes)
    bruto = hashlib.sha256(f"{core.get('ndf_id', '')}|{payload_hash}".encode("utf-8")).digest()
    codigo = "NDF-" + base64.b32encode(bruto).decode("ascii").rstrip("=")[:20]

    envelope_path = root / "envelope.json"
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    envelope["payload_hash"] = payload_hash
    envelope["validation_code"] = codigo
    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")

    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["payload_hash"] = payload_hash
    manifest["validation_code"] = codigo

    # NDF-PKG-003 exige `hash_sha256` de *cada* ficheiro, pelo que o inventário
    # cobre tudo o que está no pacote — README incluído. A única exclusão é o
    # próprio manifesto, cujo digest não pode constar dele mesmo.
    inventario = []
    for ficheiro in sorted(root.rglob("*")):
        if not ficheiro.is_file() or ficheiro == manifest_path:
            continue
        inventario.append({
            "ficheiro": ficheiro.relative_to(root).as_posix(),
            "hash_sha256": digest(ficheiro.read_bytes()),
        })
    manifest["inventario"] = inventario
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")

    print(f"{root}: payload_hash={payload_hash} validation_code={codigo} "
          f"({len(inventario)} ficheiros)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pacote", type=Path, nargs="+")
    args = parser.parse_args()
    for root in args.pacote:
        if not (root / "manifest.json").is_file():
            print(f"ERRO: {root} não é um pacote (falta manifest.json)", file=sys.stderr)
            return 1
        reseal(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
