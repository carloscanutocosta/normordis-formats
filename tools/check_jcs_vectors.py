#!/usr/bin/env python3
"""Verifica os vectores agnósticos de linguagem RFC 8785."""

import hashlib
import json
import struct
from pathlib import Path

import rfc8785


ROOT = Path(__file__).parent.parent


def main() -> int:
    suite = json.loads((ROOT / "conformance/jcs/vectors.json").read_text(encoding="utf-8"))
    failed = 0
    for vector in suite["vectors"]:
        actual = rfc8785.dumps(vector["value"])
        expected = bytes.fromhex(vector["canonical_utf8_hex"])
        digest = hashlib.sha256(actual).hexdigest()
        ok = actual == expected and digest == vector["sha256"]
        print(("PASS" if ok else "FAIL"), vector["id"])
        failed += not ok
    numbers = json.loads((ROOT / "conformance/jcs/numbers.json").read_text(encoding="utf-8"))
    for ieee_hex, expected_text in numbers["vectors"]:
        value = struct.unpack(">d", bytes.fromhex(ieee_hex))[0]
        ok = rfc8785.dumps(value) == expected_text.encode("ascii")
        print(("PASS" if ok else "FAIL"), "number-" + ieee_hex)
        failed += not ok
    for ieee_hex in numbers["must_reject"]:
        value = struct.unpack(">d", bytes.fromhex(ieee_hex))[0]
        try:
            rfc8785.dumps(value)
            ok = False
        except rfc8785.CanonicalizationError:
            ok = True
        print(("PASS" if ok else "FAIL"), "reject-" + ieee_hex)
        failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
