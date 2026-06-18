#!/usr/bin/env python3
"""
NORMORDIS Conformance Test Runner — normordis-spec

Valida NDF-core e NCRTF contra os JSON Schemas e regras semânticas adicionais.

Uso:
    python3 tools/validate.py                      # corre NDF + NCRTF
    python3 tools/validate.py path/to/ndf.json     # valida ficheiro NDF específico
    python3 tools/validate.py --valid-only          # apenas casos válidos (ambas as suites)
    python3 tools/validate.py --invalid-only        # apenas casos inválidos
    python3 tools/validate.py --format ndf          # apenas suite NDF
    python3 tools/validate.py --format ncrtf        # apenas suite NCRTF

Requisitos:
    pip install jsonschema
"""

import json
import sys
import argparse
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, SchemaError
except ImportError:
    print("ERRO: jsonschema não instalado. Execute: pip install jsonschema")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
NDF_SCHEMA_PATH   = REPO_ROOT / "specs/ndf/schema/ndf-core.schema.json"
NCRTF_SCHEMA_PATH = REPO_ROOT / "specs/ncrtf/schemas/ncrtf.schema.json"
NDF_VALID_DIR     = REPO_ROOT / "conformance/ndf/valid"
NDF_INVALID_DIR   = REPO_ROOT / "conformance/ndf/invalid"
NCRTF_VALID_DIR   = REPO_ROOT / "conformance/ncrtf/valid"
NCRTF_INVALID_DIR = REPO_ROOT / "conformance/ncrtf/invalid"

CANONICAL_MARKS_ORDER = ["bold", "code", "italic", "strikethrough", "subscript", "superscript", "underline"]

GREEN  = "\033[32m"
RED    = "\033[31m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
SEP    = "=" * 60


# ── schema cache ──────────────────────────────────────────────────────────────

_schema_cache: dict = {}

def _load_schema(path: Path) -> dict | None:
    if path not in _schema_cache:
        if not path.exists():
            return None
        with open(path, encoding="utf-8") as f:
            _schema_cache[path] = json.load(f)
    return _schema_cache[path]


# ── NCRTF semantic checks ─────────────────────────────────────────────────────

def check_ncrtf_value(value: dict, path: str) -> list[str]:
    """Valida um valor NCRTF: schema + regras semânticas R1, R2, exclusão subscript/superscript."""
    errors = []
    schema = _load_schema(NCRTF_SCHEMA_PATH)
    if schema is None:
        return []

    try:
        validator = Draft202012Validator(schema)
        for e in validator.iter_errors(value):
            field = "/".join(str(p) for p in e.absolute_path)
            errors.append(f"{path}: NCRTF schema — {e.message}" + (f" (campo: {field})" if field else ""))
    except SchemaError as e:
        errors.append(f"{path}: NCRTF schema inválido — {e.message}")
        return errors

    errors.extend(_check_ncrtf_nodes(value.get("content", []), f"{path}.content"))
    return errors


def _check_ncrtf_nodes(nodes: list, path: str) -> list[str]:
    errors = []
    errors.extend(_check_r2_contiguity(nodes, path))
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        np = f"{path}[{i}]"
        t  = node.get("type")
        if t == "text":
            errors.extend(_check_ncrtf_text(node, np))
        elif t in ("paragraph", "heading", "blockquote"):
            errors.extend(_check_ncrtf_nodes(node.get("content", []), f"{np}.content"))
        elif t == "list":
            for j, item in enumerate(node.get("content", [])):
                if isinstance(item, dict) and item.get("type") == "list_item":
                    errors.extend(_check_ncrtf_nodes(item.get("content", []), f"{np}.content[{j}].content"))
        elif t == "list_item":
            errors.extend(_check_ncrtf_nodes(node.get("content", []), f"{np}.content"))
        elif t == "link":
            errors.extend(_check_ncrtf_nodes(node.get("content", []), f"{np}.content"))
        # table cells are plain strings in v2.0.0 — no NCRTF nodes inside
    return errors


def _check_r2_contiguity(nodes: list, path: str) -> list[str]:
    """R2: nós text contíguos com marcas idênticas E font_family idêntico devem ser fundidos."""
    errors = []
    for i in range(len(nodes) - 1):
        a, b = nodes[i], nodes[i + 1]
        if not (isinstance(a, dict) and isinstance(b, dict)):
            continue
        if a.get("type") != "text" or b.get("type") != "text":
            continue
        same_marks = tuple(a.get("marks") or []) == tuple(b.get("marks") or [])
        same_font  = a.get("font_family") == b.get("font_family")
        if same_marks and same_font:
            errors.append(
                f"{path}[{i}]+[{i+1}]: nós 'text' contíguos com marcas e font_family idênticos "
                f"devem ser fundidos — '{a.get('text','')}' e '{b.get('text','')}' (SPEC.md §8.2, R2)"
            )
    return errors


def _check_ncrtf_text(node: dict, path: str) -> list[str]:
    errors = []
    marks = node.get("marks")
    if not marks:
        return errors

    # R1 — ordem canónica (bold, code, italic, strikethrough, subscript, superscript, underline)
    expected = [m for m in CANONICAL_MARKS_ORDER if m in marks]
    if marks != expected:
        errors.append(
            f"{path}: marks fora da ordem canónica — encontrado {marks}, "
            f"esperado {expected} (SPEC.md §6.2, R1)"
        )

    # R6 — exclusão mútua subscript / superscript
    if "subscript" in marks and "superscript" in marks:
        errors.append(
            f"{path}: 'subscript' e 'superscript' não podem coexistir no mesmo nó (SPEC.md §6.1, R6)"
        )

    return errors


# ── NDF semantic checks ───────────────────────────────────────────────────────

def check_ndf_semantic(doc: dict) -> list[str]:
    errors = []

    meta = doc.get("metadados", {})
    if meta.get("contem_dados_pessoais") is True:
        if not meta.get("categorias_dados_pessoais"):
            errors.append(
                "metadados.categorias_dados_pessoais deve ter pelo menos 1 item "
                "quando contem_dados_pessoais é true (§2.7.2)"
            )
        if meta.get("base_legal_conservacao") is None:
            errors.append(
                "metadados.base_legal_conservacao é obrigatório "
                "quando contem_dados_pessoais é true (§2.7.2, §1.6)"
            )

    avaliacao = doc.get("avaliacao", {})
    tcr = avaliacao.get("tipo_classificacao_ref", "")
    if tcr and "/" not in tcr:
        errors.append(
            f"avaliacao.tipo_classificacao_ref '{tcr}' deve seguir o formato "
            "'<instrumento>/<codigo_classe>' (§3.2.1)"
        )

    pca = avaliacao.get("prazo_conservacao_administrativa", {})
    if pca.get("forma_contagem") == "outro" and not pca.get("forma_contagem_detalhe"):
        errors.append(
            "avaliacao.prazo_conservacao_administrativa.forma_contagem_detalhe é "
            "obrigatório quando forma_contagem é 'outro' (§3.3)"
        )

    ndt_ref = doc.get("ndt_version_ref", "")
    if ndt_ref and "@" not in ndt_ref:
        errors.append(
            f"ndt_version_ref '{ndt_ref}' deve seguir o formato '<schema_id>@<versao>' (§2.6)"
        )

    documento = doc.get("documento", {})
    if isinstance(documento, dict):
        for field_name, field_value in documento.items():
            if isinstance(field_value, dict) and "ncrtf_version" in field_value:
                errors.extend(check_ncrtf_value(field_value, f"documento.{field_name}"))

    return errors


# ── shared helpers ────────────────────────────────────────────────────────────

def strip_meta(obj):
    """Remove campos _* (metadados de teste) antes de validar."""
    if isinstance(obj, dict):
        return {k: strip_meta(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [strip_meta(v) for v in obj]
    return obj


def _print_result(name: str, ok: bool, expect_valid: bool, errors: list, expected_error: str = ""):
    if expect_valid and ok:
        print(f"  {GREEN}PASS{RESET}  {name}")
    elif not expect_valid and not ok:
        print(f"  {GREEN}PASS{RESET}  {name}  (rejeitado como esperado)")
    elif expect_valid and not ok:
        print(f"  {RED}FAIL{RESET}  {name}  (esperado válido, mas tem erros)")
        for e in errors[:3]:
            print(f"        → {e}")
    else:
        print(f"  {RED}FAIL{RESET}  {name}  (esperado inválido, mas foi aceite)")
        if expected_error:
            print(f"        Esperado: {expected_error}")


# ── NDF file validator ────────────────────────────────────────────────────────

def validate_ndf_file(path: Path, schema: dict, expect_valid: bool) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  {RED}ERRO JSON{RESET}  {path.name}: {e}")
        return not expect_valid

    expected_error = raw.get("_expected_error", "")
    doc = strip_meta(raw)

    schema_errors = []
    try:
        schema_errors = list(Draft202012Validator(schema).iter_errors(doc))
    except SchemaError as e:
        print(f"  {RED}ERRO SCHEMA{RESET} {path.name}: schema inválido — {e.message}")
        return False

    semantic = check_ndf_semantic(doc) if not schema_errors else []
    all_errors = [e.message for e in schema_errors] + semantic
    is_valid = not all_errors

    _print_result(path.name, is_valid, expect_valid, all_errors, expected_error)
    return is_valid == expect_valid


# ── NCRTF file validator ──────────────────────────────────────────────────────

def validate_ncrtf_file(path: Path, expect_valid: bool) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  {RED}ERRO JSON{RESET}  {path.name}: {e}")
        return not expect_valid

    expected_error = raw.get("_expected_error", "")
    doc = strip_meta(raw)
    errors = check_ncrtf_value(doc, "ncrtf")
    is_valid = not errors

    _print_result(path.name, is_valid, expect_valid, errors, expected_error)
    return is_valid == expect_valid


# ── suite runners ─────────────────────────────────────────────────────────────

def run_ndf_suite(valid_only=False, invalid_only=False) -> tuple[int, int]:
    schema = _load_schema(NDF_SCHEMA_PATH)
    if schema is None:
        print(f"ERRO: schema NDF não encontrado em {NDF_SCHEMA_PATH}")
        sys.exit(1)

    passed = failed = 0

    if not invalid_only:
        print(f"\n{BOLD}{SEP}{RESET}")
        print(f"{BOLD}NDF — CASOS VÁLIDOS{RESET} — devem ser aceites")
        print(SEP)
        for p in sorted(NDF_VALID_DIR.glob("*.json")):
            if validate_ndf_file(p, schema, True): passed += 1
            else:                                   failed += 1

    if not valid_only:
        print(f"\n{BOLD}{SEP}{RESET}")
        print(f"{BOLD}NDF — CASOS INVÁLIDOS{RESET} — devem ser rejeitados")
        print(SEP)
        for p in sorted(NDF_INVALID_DIR.glob("*.json")):
            if validate_ndf_file(p, schema, False): passed += 1
            else:                                    failed += 1

    return passed, failed


def run_ncrtf_suite(valid_only=False, invalid_only=False) -> tuple[int, int]:
    if _load_schema(NCRTF_SCHEMA_PATH) is None:
        print(f"ERRO: schema NCRTF não encontrado em {NCRTF_SCHEMA_PATH}")
        sys.exit(1)

    passed = failed = 0

    if not invalid_only and NCRTF_VALID_DIR.exists():
        print(f"\n{BOLD}{SEP}{RESET}")
        print(f"{BOLD}NCRTF — CASOS VÁLIDOS{RESET} — devem ser aceites")
        print(SEP)
        for p in sorted(NCRTF_VALID_DIR.glob("*.json")):
            if validate_ncrtf_file(p, True):  passed += 1
            else:                              failed += 1

    if not valid_only and NCRTF_INVALID_DIR.exists():
        print(f"\n{BOLD}{SEP}{RESET}")
        print(f"{BOLD}NCRTF — CASOS INVÁLIDOS{RESET} — devem ser rejeitados")
        print(SEP)
        for p in sorted(NCRTF_INVALID_DIR.glob("*.json")):
            if validate_ncrtf_file(p, False): passed += 1
            else:                              failed += 1

    return passed, failed


def _print_total(passed: int, failed: int):
    colour = GREEN if failed == 0 else RED
    print(f"\n{BOLD}{SEP}{RESET}")
    print(f"{colour}{BOLD}{passed}/{passed+failed} passed{RESET}", end="")
    print(f"  ({failed} failed)" if failed else "")
    print(SEP)


# ── single file ───────────────────────────────────────────────────────────────

def validate_single(path: Path) -> bool:
    schema = _load_schema(NDF_SCHEMA_PATH)
    if schema is None:
        print(f"ERRO: schema NDF não encontrado em {NDF_SCHEMA_PATH}")
        sys.exit(1)
    print(f"\nA validar: {path}")
    return validate_ndf_file(path, schema, expect_valid=True)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="NORMORDIS Conformance Test Runner")
    parser.add_argument("file", nargs="?", type=Path, help="Ficheiro NDF-core a validar.")
    parser.add_argument("--valid-only",   action="store_true")
    parser.add_argument("--invalid-only", action="store_true")
    parser.add_argument("--format", choices=["ndf", "ncrtf", "all"], default="all",
                        help="Suite a correr (default: all)")
    args = parser.parse_args()

    if args.file:
        ok = validate_single(args.file)
        sys.exit(0 if ok else 1)

    p = f = 0
    if args.format in ("ndf", "all"):
        np, nf = run_ndf_suite(args.valid_only, args.invalid_only)
        p += np; f += nf
    if args.format in ("ncrtf", "all"):
        np, nf = run_ncrtf_suite(args.valid_only, args.invalid_only)
        p += np; f += nf

    _print_total(p, f)
    sys.exit(0 if f == 0 else 1)


if __name__ == "__main__":
    main()
