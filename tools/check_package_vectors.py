#!/usr/bin/env python3
"""Executa vetores negativos reproduzíveis sobre o exemplo .ndfpkg."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from validate import validate_package_dir


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "specs/ndf/examples/ndfpkg-example"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_inventory_hash(root: Path, relative: str) -> None:
    manifest_path = root / "manifest.json"
    manifest = load(manifest_path)
    digest = "sha256:" + hashlib.sha256((root / relative).read_bytes()).hexdigest()
    for item in manifest["inventario"]:
        if item["ficheiro"] == relative:
            item["hash_sha256"] = digest
            dump(manifest_path, manifest)
            return
    raise RuntimeError(f"entrada ausente no inventário: {relative}")


def cases(root: Path):
    yield "PKG-NEG-001-hash-alterado", lambda p: _tamper_hash(p)
    yield "PKG-NEG-002-ficheiro-nao-inventariado", lambda p: (p / "extra.bin").write_bytes(b"x")
    yield "PKG-NEG-003-inventario-duplicado", lambda p: _duplicate_item(p)
    yield "PKG-NEG-004-caminho-inseguro", lambda p: _unsafe_path(p)
    yield "PKG-NEG-005-ndt-ausente", lambda p: (p / "ndt/oficio-generico@2.0.0.ndt.json").unlink()
    yield "PKG-NEG-006-identidade-ndt-divergente", lambda p: _mismatch_ndt(p)
    yield "PKG-NEG-007-envelope-sem-timestamps", lambda p: _remove_timestamps(p)


def _tamper_hash(root: Path) -> None:
    manifest = load(root / "manifest.json")
    manifest["inventario"][0]["hash_sha256"] = "sha256:" + "0" * 64
    dump(root / "manifest.json", manifest)


def _duplicate_item(root: Path) -> None:
    manifest = load(root / "manifest.json")
    manifest["inventario"].append(dict(manifest["inventario"][0]))
    dump(root / "manifest.json", manifest)


def _unsafe_path(root: Path) -> None:
    manifest = load(root / "manifest.json")
    manifest["inventario"].append({
        "ficheiro": "../escape.json",
        "hash_sha256": "sha256:" + "0" * 64,
    })
    dump(root / "manifest.json", manifest)


def _mismatch_ndt(root: Path) -> None:
    relative = "ndt/oficio-generico@2.0.0.ndt.json"
    path = root / relative
    ndt = load(path)
    ndt["schema_id"] = "outro-template"
    dump(path, ndt)
    update_inventory_hash(root, relative)


def _remove_timestamps(root: Path) -> None:
    relative = "envelope.json"
    path = root / relative
    envelope = load(path)
    envelope.pop("timestamps", None)
    dump(path, envelope)
    update_inventory_hash(root, relative)


def main() -> int:
    if not validate_package_dir(SOURCE):
        print("FAIL package baseline")
        return 1
    failed = 0
    with tempfile.TemporaryDirectory(prefix="normordis-package-") as tmp:
        base = Path(tmp)
        for name, mutate in cases(base):
            target = base / name
            shutil.copytree(SOURCE, target)
            mutate(target)
            if validate_package_dir(target):
                print(f"FAIL {name}: pacote inválido foi aceite")
                failed += 1
            else:
                print(f"PASS {name}: rejeitado como esperado")
    print(f"PASS package vectors: {7 - failed}/7" if not failed else f"FAIL package vectors: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
