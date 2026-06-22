#!/usr/bin/env python3
"""Valida uma cadeia de custódia NDF (implementação Python de referência)."""

import argparse
import hashlib
import json
from pathlib import Path

import rfc8785
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).parent.parent


def validate(events):
    schema = json.loads((ROOT / "specs/ndf/schemas/custody-event.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    previous = None
    ndf_id = None
    for index, event in enumerate(events):
        errors.extend(f"evento {index}: {e.message}" for e in validator.iter_errors(event))
        if event.get("sequence") != index:
            errors.append(f"evento {index}: sequence não contígua")
        if event.get("previous_event_hash") != previous:
            errors.append(f"evento {index}: previous_event_hash incorrecto")
        if ndf_id is not None and event.get("ndf_id") != ndf_id:
            errors.append(f"evento {index}: ndf_id mudou dentro da cadeia")
        ndf_id = event.get("ndf_id")
        unsigned = {k: v for k, v in event.items() if k != "event_hash"}
        actual = "sha256:" + hashlib.sha256(rfc8785.dumps(unsigned)).hexdigest()
        if event.get("event_hash") != actual:
            errors.append(f"evento {index}: event_hash incorrecto")
        previous = event.get("event_hash")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    events = json.loads(args.file.read_text(encoding="utf-8"))
    errors = validate(events)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
