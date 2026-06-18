#!/usr/bin/env python3
"""
NDF Conformance Test Runner — normordis-spec

Valida NDF-core JSON files contra o JSON Schema e regras semânticas adicionais.

Uso:
    python tools/validate.py                     # corre toda a suite de conformidade
    python tools/validate.py path/to/ndf.json    # valida um ficheiro específico
    python tools/validate.py --valid-only        # apenas casos válidos
    python tools/validate.py --invalid-only      # apenas casos inválidos

Requisitos:
    pip install jsonschema
"""

import json
import sys
import re
import argparse
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERRO: jsonschema não instalado. Execute: pip install jsonschema")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "specs/ndf/schema/ndf-core.schema.json"
VALID_DIR = REPO_ROOT / "conformance/ndf/valid"
INVALID_DIR = REPO_ROOT / "conformance/ndf/invalid"

ANSI_GREEN = "\033[32m"
ANSI_RED = "\033[31m"
ANSI_YELLOW = "\033[33m"
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"


def strip_meta(obj):
    """Remove campos _* (metadados de teste) antes de validar."""
    if isinstance(obj, dict):
        return {k: strip_meta(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [strip_meta(v) for v in obj]
    return obj


def check_semantic_rules(doc: dict) -> list[str]:
    """
    Regras semânticas que o JSON Schema não captura.
    Devolve lista de erros (vazia se tudo correcto).
    """
    errors = []

    # Regra: contem_dados_pessoais: true exige categorias_dados_pessoais não-vazia
    meta = doc.get("metadados", {})
    if meta.get("contem_dados_pessoais") is True:
        cats = meta.get("categorias_dados_pessoais", [])
        if not cats:
            errors.append(
                "metadados.categorias_dados_pessoais deve ter pelo menos 1 item "
                "quando contem_dados_pessoais é true (§2.7.2)"
            )
        if meta.get("base_legal_conservacao") is None:
            errors.append(
                "metadados.base_legal_conservacao é obrigatório "
                "quando contem_dados_pessoais é true (§2.7.2, §1.6)"
            )

    # Regra: tipo_classificacao_ref deve seguir formato <instrumento>/<codigo>
    avaliacao = doc.get("avaliacao", {})
    tcr = avaliacao.get("tipo_classificacao_ref", "")
    if tcr and "/" not in tcr:
        errors.append(
            f"avaliacao.tipo_classificacao_ref '{tcr}' deve seguir o formato "
            "'<instrumento>/<codigo_classe>' (§3.2.1)"
        )

    # Regra: forma_contagem 'outro' exige forma_contagem_detalhe
    pca = avaliacao.get("prazo_conservacao_administrativa", {})
    if pca.get("forma_contagem") == "outro" and not pca.get("forma_contagem_detalhe"):
        errors.append(
            "avaliacao.prazo_conservacao_administrativa.forma_contagem_detalhe é "
            "obrigatório quando forma_contagem é 'outro' (§3.3)"
        )

    # Regra: ndt_version_ref deve seguir formato <id>@<versao>
    ndt_ref = doc.get("ndt_version_ref", "")
    if ndt_ref and "@" not in ndt_ref:
        errors.append(
            f"ndt_version_ref '{ndt_ref}' deve seguir o formato "
            "'<schema_id>@<versao_impresso>' (§2.6)"
        )

    # Regra: nivel_assinatura 'qualificada' e entidade_produtora sem nif — aviso
    # (não é erro bloqueante, mas é recomendado)

    return errors


def validate_file(path: Path, schema: dict, expect_valid: bool) -> bool:
    """
    Valida um ficheiro. Devolve True se o resultado foi o esperado.
    """
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  {ANSI_RED}ERRO JSON{ANSI_RESET}  {path.name}: {e}")
        return not expect_valid

    expected_error = raw.get("_expected_error", "")
    doc = strip_meta(raw)

    schema_errors = []
    try:
        validator = Draft202012Validator(schema)
        schema_errors = list(validator.iter_errors(doc))
    except SchemaError as e:
        print(f"  {ANSI_RED}ERRO SCHEMA{ANSI_RESET} {path.name}: schema inválido — {e.message}")
        return False

    semantic_errors = check_semantic_rules(doc) if not schema_errors else []
    all_errors = schema_errors + [type("E", (), {"message": e})() for e in semantic_errors]

    is_valid = len(all_errors) == 0

    if expect_valid and is_valid:
        print(f"  {ANSI_GREEN}PASS{ANSI_RESET}  {path.name}")
        return True
    elif not expect_valid and not is_valid:
        print(f"  {ANSI_GREEN}PASS{ANSI_RESET}  {path.name}  (rejeitado como esperado)")
        return True
    elif expect_valid and not is_valid:
        print(f"  {ANSI_RED}FAIL{ANSI_RESET}  {path.name}  (esperado válido, mas tem erros)")
        for e in all_errors[:3]:
            print(f"        → {e.message}")
        return False
    else:
        print(f"  {ANSI_RED}FAIL{ANSI_RESET}  {path.name}  (esperado inválido, mas foi aceite)")
        if expected_error:
            print(f"        Esperado: {expected_error}")
        return False


def run_suite(valid_only=False, invalid_only=False) -> bool:
    if not SCHEMA_PATH.exists():
        print(f"ERRO: schema não encontrado em {SCHEMA_PATH}")
        sys.exit(1)

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)

    passed = 0
    failed = 0

    if not invalid_only:
        print(f"\n{ANSI_BOLD}{'='*60}{ANSI_RESET}")
        print(f"{ANSI_BOLD}CASOS VÁLIDOS{ANSI_RESET} — devem ser aceites")
        print(f"{'='*60}")
        for path in sorted(VALID_DIR.glob("*.json")):
            ok = validate_file(path, schema, expect_valid=True)
            if ok:
                passed += 1
            else:
                failed += 1

    if not valid_only:
        print(f"\n{ANSI_BOLD}{'='*60}{ANSI_RESET}")
        print(f"{ANSI_BOLD}CASOS INVÁLIDOS{ANSI_RESET} — devem ser rejeitados")
        print(f"{'='*60}")
        for path in sorted(INVALID_DIR.glob("*.json")):
            ok = validate_file(path, schema, expect_valid=False)
            if ok:
                passed += 1
            else:
                failed += 1

    total = passed + failed
    colour = ANSI_GREEN if failed == 0 else ANSI_RED
    print(f"\n{ANSI_BOLD}{'='*60}{ANSI_RESET}")
    print(f"{colour}{ANSI_BOLD}{passed}/{total} passed{ANSI_RESET}", end="")
    if failed:
        print(f"  ({failed} failed)")
    else:
        print()
    print(f"{'='*60}")

    return failed == 0


def validate_single(path: Path) -> bool:
    if not SCHEMA_PATH.exists():
        print(f"ERRO: schema não encontrado em {SCHEMA_PATH}")
        sys.exit(1)

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)

    print(f"\nA validar: {path}")
    ok = validate_file(path, schema, expect_valid=True)
    return ok


def main():
    parser = argparse.ArgumentParser(
        description="NDF Conformance Test Runner — normordis-spec"
    )
    parser.add_argument(
        "file", nargs="?", type=Path,
        help="Ficheiro NDF-core a validar. Se omitido, corre toda a suite."
    )
    parser.add_argument("--valid-only", action="store_true", help="Apenas casos válidos.")
    parser.add_argument("--invalid-only", action="store_true", help="Apenas casos inválidos.")
    args = parser.parse_args()

    if args.file:
        ok = validate_single(args.file)
    else:
        ok = run_suite(valid_only=args.valid_only, invalid_only=args.invalid_only)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
