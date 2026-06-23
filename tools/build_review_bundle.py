#!/usr/bin/env python3
"""Constrói um dossier autocontido para revisão pública."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build/review"
STAGING = BUILD / "normordis-formats-review"


def git(*args: str) -> str:
    return subprocess.check_output(("git", *args), cwd=ROOT, text=True).strip()


def selected_files():
    roots = [
        ROOT / "specs",
        ROOT / "conformance",
        ROOT / "docs/architecture",
        ROOT / "docs/normalization",
        ROOT / "docs/benchmarks",
    ]
    top = [
        "README.md", "GOVERNANCE.md", "CONFORMANCE.md", "CONTRIBUTING.md",
        "NORMALIZATION.md", "VERSIONING.md", "ROADMAP.md", "CHANGELOG.md",
        "LICENSE-SPEC",
    ]
    files = [ROOT / name for name in top]
    for directory in roots:
        files.extend(path for path in directory.rglob("*") if path.is_file())
    return sorted(set(files))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()
    dirty = bool(git("status", "--porcelain"))
    if dirty and not args.allow_dirty:
        print("FAIL: árvore Git com alterações; use --allow-dirty apenas para pré-visualização")
        return 1

    shutil.rmtree(BUILD, ignore_errors=True)
    STAGING.mkdir(parents=True)
    entries = []
    for source in selected_files():
        relative = source.relative_to(ROOT)
        target = STAGING / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        entries.append({
            "path": relative.as_posix(),
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "bytes": source.stat().st_size,
        })
    manifest = {
        "bundle_version": "1.0.0",
        "source_commit": git("rev-parse", "HEAD"),
        "dirty_preview": dirty,
        "documents": entries,
    }
    (STAGING / "REVIEW-MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    archive = shutil.make_archive(str(BUILD / "normordis-formats-review"), "zip", STAGING)
    print(f"PASS review bundle: {len(entries)} ficheiros; {Path(archive).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
