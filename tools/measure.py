#!/usr/bin/env python3
"""Mede tamanho bruto e gzip de ficheiros, de forma determinística."""

import argparse
import gzip
import json
from pathlib import Path


def files_under(paths):
    for path in paths:
        if path.is_file():
            yield path, path.name
        elif path.is_dir():
            for child in sorted(p for p in path.rglob("*") if p.is_file()):
                yield child, str(child.relative_to(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    rows = []
    for path, label in files_under(args.paths):
        data = path.read_bytes()
        compressed = gzip.compress(data, compresslevel=9, mtime=0)
        rows.append({"file": label, "bytes": len(data), "gzip_bytes": len(compressed)})
    print(json.dumps({
        "files": rows,
        "total_bytes": sum(r["bytes"] for r in rows),
        "total_gzip_bytes": sum(r["gzip_bytes"] for r in rows)
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
