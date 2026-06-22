#!/usr/bin/env python3
"""Implementação Python não normativa da canonicalização RFC 8785 (JCS).

O contrato interoperável é constituído pela RFC e pelos vectores publicados em
conformance/jcs; outras linguagens não dependem deste programa.
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


def _no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"chave JSON duplicada: {key!r}")
        result[key] = value
    return result


def load_json(path: Path):
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("BOM UTF-8 não permitido")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicates)


def canonicalize(value) -> bytes:
    return rfc8785.dumps(value)


def payload_hash(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def validation_code(ndf_id: str, digest: str) -> str:
    raw = hashlib.sha256(f"{ndf_id}|{digest}".encode("utf-8")).digest()
    return "NDF-" + base64.b32encode(raw).decode("ascii").rstrip("=")[:20]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--hash", action="store_true", help="Imprime SHA-256 dos bytes JCS.")
    parser.add_argument("--validation-code", action="store_true")
    parser.add_argument("--verify", action="store_true", help="Confirma que o ficheiro já contém bytes JCS exactos.")
    args = parser.parse_args()

    try:
        value = load_json(args.file)
        canonical = canonicalize(value)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, rfc8785.CanonicalizationError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    digest = payload_hash(canonical)
    if args.verify:
        if args.file.read_bytes() != canonical:
            print("ERRO: o ficheiro não está em representação JCS canónica", file=sys.stderr)
            return 1
        print("OK: JCS canónico")
    elif args.validation_code:
        if not isinstance(value, dict) or not isinstance(value.get("ndf_id"), str):
            print("ERRO: validation_code requer ndf_id no objecto raiz", file=sys.stderr)
            return 1
        print(validation_code(value["ndf_id"], digest))
    elif args.hash:
        print(digest)
    else:
        sys.stdout.buffer.write(canonical)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
