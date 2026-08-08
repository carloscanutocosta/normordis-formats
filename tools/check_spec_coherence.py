#!/usr/bin/env python3
"""Guardrails de coerência entre SPEC, schemas e artefactos executáveis.

Origem: revisão adversarial pré-RC (`docs/reports/NDF-PRE-RC-REVIEW.md`). O
padrão que produziu 16 achados foi sempre o mesmo — a definição principal é
alterada e as cláusulas secundárias ficam para trás. Uma suite de
conformidade verde não deteta isso: os 58 casos passavam enquanto três
blocos JSON da própria SPEC eram inválidos.

Verifica:
  C1  blocos JSON normativos da SPEC validam contra o schema correspondente
  C2  campos declarados nos schemas aparecem documentados na SPEC
  C3  referências §X.Y resolvem para secções existentes (por documento)
  C4  enums deliberadamente duplicados entre schemas mantêm-se idênticos
  C5  propriedades removidas não reaparecem em specs/ ou conformance/
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specs/ndf/SPEC.md"

SCHEMAS = {
    "ndf-core": ROOT / "specs/ndf/schemas/ndf-core.schema.json",
    "envelope": ROOT / "specs/ndf/schemas/envelope.schema.json",
    "manifest": ROOT / "specs/ndf/schemas/manifest.schema.json",
    "custody-event": ROOT / "specs/ndf/schemas/custody-event.schema.json",
}

# Propriedades removidas por decisão arquitetural — não devem reaparecer.
# (nome, ADR que as removeu)
REMOVED_PROPERTIES = [
    ("versao_anterior", "ADR-011"),
    ("hash_anterior", "ADR-011"),
]

# Campos cuja ausência da SPEC é aceite (internos ou cobertos por prosa geral).
DOCUMENTATION_EXEMPT = {
    "display_name",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_properties(schema, out=None) -> set[str]:
    out = set() if out is None else out
    if not isinstance(schema, dict):
        return out
    for k, v in schema.get("properties", {}).items():
        out.add(k)
        schema_properties(v, out)
    for key in ("items", "then", "else", "if", "not"):
        if key in schema:
            schema_properties(schema[key], out)
    for key in ("$defs", "definitions"):
        for sub in schema.get(key, {}).values():
            schema_properties(sub, out)
    for key in ("allOf", "anyOf", "oneOf"):
        for sub in schema.get(key, []):
            schema_properties(sub, out)
    return out


def json_blocks(text: str):
    """Devolve (linha_inicial, secção, objeto) para cada bloco ```json parseável."""
    lines = text.splitlines()
    blocks, cur, start = [], None, None
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```json"):
            cur, start = [], n
            continue
        if cur is not None and line.strip() == "```":
            blocks.append((start, "\n".join(cur)))
            cur = None
            continue
        if cur is not None:
            cur.append(line)

    def section_of(lineno: int) -> str:
        sec = "?"
        for n, line in enumerate(lines, 1):
            if n > lineno:
                break
            m = re.match(r"^#{2,4}\s+(\d+(?:\.\d+)*)", line)
            if m:
                sec = m.group(1)
        return sec

    for start, body in blocks:
        try:
            obj = json.loads(body)
        except json.JSONDecodeError:
            continue  # blocos ilustrativos com elipses ou comentários
        yield start, section_of(start), obj


def classify(obj) -> str | None:
    """Identifica a que schema um bloco JSON completo corresponde."""
    if not isinstance(obj, dict):
        return None
    keys = set(obj)
    if "ndfpkg_version" in keys or "inventario" in keys:
        return "manifest"
    if "custody_event_version" in keys or "event_hash" in keys:
        return "custody-event"
    if "ndf_version" in keys:
        return "ndf-core"
    if {"validation_code", "payload_hash"} <= keys:
        return "envelope"
    return None


def c1_spec_blocks(schemas, failures):
    spec = SPEC.read_text(encoding="utf-8")
    checked = 0
    for start, sec, obj in json_blocks(spec):
        target = classify(obj)
        if not target:
            continue
        checked += 1
        validator = Draft202012Validator(schemas[target], format_checker=FormatChecker())
        for e in validator.iter_errors(obj):
            failures.append(
                f"C1 SPEC.md §{sec} (linha {start}): bloco JSON não valida "
                f"contra {target}.schema.json — {e.message}"
            )
    return checked


def c2_documented_fields(schemas, failures):
    """Um campo conta como documentado se aparecer em prosa (`campo`) ou como
    chave num exemplo normativo JSON ("campo":) da SPEC."""
    spec = SPEC.read_text(encoding="utf-8")
    checked = 0
    for name, schema in schemas.items():
        for field in sorted(schema_properties(schema)):
            if field in DOCUMENTATION_EXEMPT:
                continue
            checked += 1
            if f"`{field}`" not in spec and f'"{field}"' not in spec:
                failures.append(
                    f"C2 {name}.schema.json declara `{field}`, "
                    f"que nunca é mencionado em SPEC.md (nem em prosa nem em exemplo)"
                )
    return checked


def c3_section_refs(failures):
    checked = 0
    for spec_path in sorted(ROOT.glob("specs/*/SPEC.md")):
        text = spec_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        existing = set()
        for line in lines:
            m = re.match(r"^#{2,4}\s+(\d+(?:\.\d+)*)\b", line)
            if m:
                existing.add(m.group(1))
        in_code = False
        for n, line in enumerate(lines, 1):
            if line.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            # ignora referências explicitamente cruzadas para outro documento
            # (ex.: "definida no NDT v2.0.0 §5.8", "ver NDF especificação §4.6")
            if re.search(r"\b(especificação|SPEC\.md|NDT|NCRTF|NDF)\b[^§]{0,40}§", line):
                continue
            for m in re.finditer(r"§(\d+(?:\.\d+)*)", line):
                checked += 1
                if m.group(1) not in existing:
                    failures.append(
                        f"C3 {spec_path.relative_to(ROOT)}:{n} refere §{m.group(1)}, "
                        f"que não existe neste documento"
                    )
    return checked


def c4_duplicated_enums(schemas, failures):
    """Enums deliberadamente duplicados (F16) — verificar que não derivam."""
    pairs = [
        ("estado", ["envelope", "manifest"]),
        ("nivel_assinatura", ["manifest"]),
    ]
    checked = 0
    for field, owners in pairs:
        values = {}
        for owner in owners:
            prop = schemas[owner].get("properties", {}).get(field, {})
            enum = prop.get("enum")
            if enum is not None:
                values[owner] = enum
        if len(values) > 1:
            checked += 1
            distinct = {tuple(v) for v in values.values()}
            if len(distinct) > 1:
                failures.append(
                    f"C4 enum `{field}` divergiu entre schemas: {values}"
                )
    return checked


def c5_removed_properties(failures):
    checked = 0
    targets = list((ROOT / "specs").rglob("*.json")) + \
              list((ROOT / "specs").rglob("*.md")) + \
              list((ROOT / "conformance").rglob("*.json"))
    for prop, adr in REMOVED_PROPERTIES:
        checked += 1
        for path in targets:
            if "/build/" in str(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if prop in text:
                failures.append(
                    f"C5 `{prop}` foi removido por {adr} mas reaparece em "
                    f"{path.relative_to(ROOT)}"
                )
    return checked


def main() -> int:
    schemas = {n: load(p) for n, p in SCHEMAS.items()}
    failures: list[str] = []

    n1 = c1_spec_blocks(schemas, failures)
    n2 = c2_documented_fields(schemas, failures)
    n3 = c3_section_refs(failures)
    n4 = c4_duplicated_enums(schemas, failures)
    n5 = c5_removed_properties(failures)

    if failures:
        for f in failures:
            print(f"FAIL {f}")
        print(f"\nFAIL spec coherence: {len(failures)} problemas")
        return 1

    print(
        f"PASS spec coherence: {n1} blocos JSON, {n2} campos de schema, "
        f"{n3} referências de secção, {n4} enums duplicados, "
        f"{n5} propriedades removidas"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
