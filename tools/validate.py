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
import base64
import hashlib
import re
from datetime import datetime
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, SchemaError, FormatChecker
except ImportError:
    print("ERRO: jsonschema não instalado. Execute: pip install -r tools/requirements.txt")
    sys.exit(1)

try:
    import rfc8785
except ImportError:
    rfc8785 = None

REPO_ROOT = Path(__file__).parent.parent
NDF_SCHEMA_PATH   = REPO_ROOT / "specs/ndf/schemas/ndf-core.schema.json"
NCRTF_SCHEMA_PATH = REPO_ROOT / "specs/ncrtf/schemas/ncrtf.schema.json"
REGISTRY_SCHEMA_DIR = REPO_ROOT / "specs/registry/schemas"
MANIFEST_SCHEMA_PATH = REPO_ROOT / "specs/ndf/schemas/manifest.schema.json"
ENVELOPE_SCHEMA_PATH = REPO_ROOT / "specs/ndf/schemas/envelope.schema.json"
NDT_SCHEMA_PATH = REPO_ROOT / "specs/ndt/schemas/ndt.schema.json"
NDF_VALID_DIR     = REPO_ROOT / "conformance/ndf/valid"
NDF_INVALID_DIR   = REPO_ROOT / "conformance/ndf/invalid"
NCRTF_VALID_DIR   = REPO_ROOT / "conformance/ncrtf/valid"
NCRTF_INVALID_DIR = REPO_ROOT / "conformance/ncrtf/invalid"
NDT_VALID_DIR     = REPO_ROOT / "conformance/ndt/valid"
NDT_EXAMPLES_DIR  = REPO_ROOT / "specs/ndt/examples"
NDT_INVALID_DIR   = REPO_ROOT / "conformance/ndt/invalid"

CANONICAL_MARKS_ORDER = ["bold", "code", "italic", "strikethrough", "subscript", "superscript", "underline"]

GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
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
        elif t == "table":
            all_rows = list(node.get("head") or []) + list(node.get("body") or [])
            if all_rows:
                expected = len(all_rows[0].get("cells") or [])
                for r, row in enumerate(all_rows[1:], 1):
                    actual = len(row.get("cells") or [])
                    if actual != expected:
                        errors.append(
                            f"{np}: tabela com número inconsistente de células — "
                            f"linha 0 tem {expected}, linha {r} tem {actual} (SPEC.md §4.5)"
                        )
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

def fmt_schema_error(e) -> str:
    """Mensagem legível para um erro de schema.

    O invariante de origem (§2.2.1) é expresso por `anyOf` na raiz — portável
    para qualquer validador Draft 2020-12, mas a mensagem nativa despeja o
    documento inteiro. Como é o erro de autoria mais provável, traduz-se.
    """
    if e.validator == "anyOf" and not list(e.absolute_path):
        return (
            "NDF-core não declara nenhuma origem do conteúdo: é necessário "
            "participantes[] com papel 'autor', 'coautor' ou 'decisor', ou "
            "proveniencia_sistema não vazio, ou proveniencia_ia.utilizada true "
            "(§2.2.1)"
        )
    field = "/".join(str(p) for p in e.absolute_path)
    return e.message + (f" (campo: {field})" if field else "")


def _resolve_tipo_schema(tipo_id: str, pkg_root: Path | None):
    """Resolve o schema do tipo documental, preferindo o que viaja no pacote.

    SPEC.md §2.9.5 e §9.3 (NDF-PKG-007): um .ndfpkg é autonomamente validável,
    logo o schema que vem em schemas/ tem precedência sobre o registo canónico.
    Devolve (schema, origem) com origem em {"pacote", "registo", None}.
    """
    if pkg_root is not None:
        in_pkg = pkg_root / "schemas" / f"{tipo_id}.schema.json"
        if in_pkg.is_file():
            return _load_schema(in_pkg), "pacote"
    in_registry = REGISTRY_SCHEMA_DIR / f"{tipo_id}.schema.json"
    if in_registry.is_file():
        return _load_schema(in_registry), "registo"
    return None, None


def check_ndf_semantic(doc: dict, pkg_root: Path | None = None) -> list[str]:
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

    iar = avaliacao.get("instrumento_avaliacao_versao_ref", "")
    if tcr and iar and tcr.split("/", 1)[0] != iar.split("/", 1)[0]:
        errors.append(
            "avaliacao.tipo_classificacao_ref e instrumento_avaliacao_versao_ref "
            "devem referenciar o mesmo instrumento (§3.2.2)"
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
    tipo_ref = meta.get("tipo_documento_ref", "")
    tipo_id = tipo_ref.rsplit("@", 1)[0] if "@" in tipo_ref else ""
    tipo_schema, origem = _resolve_tipo_schema(tipo_id, pkg_root) if tipo_id else (None, None)
    if tipo_schema is not None:
        for e in Draft202012Validator(tipo_schema, format_checker=FormatChecker()).iter_errors(documento):
            field = "/".join(str(p) for p in e.absolute_path)
            errors.append(
                f"documento não valida contra {tipo_ref} (schema do {origem}): {e.message}" +
                (f" (campo: {field})" if field else "")
            )
    elif tipo_id:
        # §2.9.5: este runner é estrito porque DETÉM o registo canónico — aqui,
        # um tipo canónico não resolúvel significa que não existe, não que o
        # leitor não lhe tem acesso. NDF-READ-018 admite, para leitores em
        # geral, tratar `documento` como opaco em vez de rejeitar; o que nunca
        # é admissível é declará-lo validado sem o ter sido, que era o
        # comportamento anterior (o caso passava em silêncio).
        # Tipo de extensão: erro dentro de um pacote (tem de lá vir), aviso num
        # ficheiro solto, onde não existe onde o resolver.
        if not tipo_id.startswith("ext."):
            errors.append(
                f"metadados.tipo_documento_ref '{tipo_ref}' não resolve em "
                f"specs/registry/schemas/{tipo_id}.schema.json (§2.9.2)"
            )
        elif pkg_root is not None:
            errors.append(
                f"metadados.tipo_documento_ref '{tipo_ref}' é uma extensão qualificada "
                f"e o pacote não contém schemas/{tipo_id}.schema.json (§2.9.5, NDF-PKG-007)"
            )

    prov_sistema = doc.get("proveniencia_sistema")
    if isinstance(prov_sistema, list):
        # §2.14.3: JCS preserva a ordem dos arrays, logo a ordem entra no
        # payload_hash. Sem ordem normativa, os mesmos factos produziriam
        # hashes diferentes. Não é exprimível em JSON Schema — nenhum
        # vocabulário Draft 2020-12 compara elementos de um array entre si.
        instantes = []
        for e in prov_sistema:
            bruto = e.get("gerado_em") if isinstance(e, dict) else None
            if not isinstance(bruto, str):
                break
            try:
                # comparar instantes, não strings: '...Z' e '...+01:00' são
                # ordenáveis entre si como datas mas não lexicograficamente
                instantes.append((datetime.fromisoformat(bruto), bruto))
            except ValueError:
                break
        if len(instantes) == len(prov_sistema):
            for i in range(1, len(instantes)):
                if instantes[i][0] < instantes[i - 1][0]:
                    errors.append(
                        f"proveniencia_sistema[{i}].gerado_em ({instantes[i][1]}) é anterior "
                        f"a proveniencia_sistema[{i - 1}].gerado_em ({instantes[i - 1][1]}) — "
                        "as entradas devem estar ordenadas cronologicamente (§2.14.3)"
                    )
                    break

    if isinstance(documento, dict):
        for field_name, field_value in documento.items():
            if isinstance(field_value, dict) and "ncrtf_version" in field_value:
                errors.extend(check_ncrtf_value(field_value, f"documento.{field_name}"))

    return errors


def check_ndf_advisories(doc: dict, pkg_root: Path | None = None) -> list[str]:
    """Verificações não-bloqueantes — produzem aviso, não erro (ex.: A7,
    coerência entre documento.sobre[] e relacoes[], SPEC.md §2.11.4)."""
    advisories = []

    # §2.9.5: num ficheiro solto não existe onde resolver um tipo de extensão —
    # o aviso regista que `documento` não foi validado contra schema nenhum.
    # Dentro de um pacote a mesma situação é erro (NDF-PKG-007).
    if pkg_root is None:
        tipo_ref = doc.get("metadados", {}).get("tipo_documento_ref", "")
        tipo_id = tipo_ref.rsplit("@", 1)[0] if "@" in tipo_ref else ""
        if tipo_id.startswith("ext."):
            schema, _ = _resolve_tipo_schema(tipo_id, None)
            if schema is None:
                advisories.append(
                    f"tipo de extensão '{tipo_ref}' não resolúvel fora de um pacote — "
                    "documento não foi validado contra nenhum schema de tipo (§2.9.5)"
                )

    documento = doc.get("documento", {})
    sobre = documento.get("sobre") if isinstance(documento, dict) else None
    relacoes = doc.get("relacoes")
    if isinstance(sobre, list) and isinstance(relacoes, list):
        sobre_ids = {item.get("ndf_id") for item in sobre if isinstance(item, dict)}
        relacoes_ids = {
            rel.get("alvo", {}).get("ndf_id")
            for rel in relacoes if isinstance(rel, dict)
        }
        if sobre_ids and relacoes_ids and sobre_ids != relacoes_ids:
            so_em_sobre = sobre_ids - relacoes_ids
            so_em_relacoes = relacoes_ids - sobre_ids
            detalhe = []
            if so_em_sobre:
                detalhe.append(f"apenas em documento.sobre[]: {sorted(so_em_sobre)}")
            if so_em_relacoes:
                detalhe.append(f"apenas em relacoes[]: {sorted(so_em_relacoes)}")
            advisories.append(
                "documento.sobre[] e relacoes[] referenciam conjuntos "
                "diferentes de ndf_id — RECOMENDA-SE coerência (§2.11.4): "
                + "; ".join(detalhe)
            )

    # §2.14.4 — a fronteira entre proveniencia_sistema (determinístico) e
    # proveniencia_ia não é mecanicamente decidível: nenhum campo declara se um
    # componente é determinístico. Só é detectável o indício de um mesmo
    # sistema aparecer nos dois blocos, que é sinal de possível contorno do
    # revisao_humana obrigatório. O requisito completo é normativo, não
    # testável — ver SPEC.md §2.14.4 e §9.1.
    prov_sistema = doc.get("proveniencia_sistema")
    prov_ia = doc.get("proveniencia_ia")
    if isinstance(prov_sistema, list) and isinstance(prov_ia, dict):
        nomes_sistema = {
            (e.get("sistema") or {}).get("nome")
            for e in prov_sistema if isinstance(e, dict)
        }
        nomes_ia = {
            (i.get("sistema") or {}).get("nome")
            for i in prov_ia.get("intervencoes") or [] if isinstance(i, dict)
        }
        comuns = sorted(n for n in nomes_sistema & nomes_ia if n)
        if comuns:
            advisories.append(
                "o mesmo sistema consta de proveniencia_sistema e de "
                f"proveniencia_ia ({', '.join(comuns)}) — um componente não "
                "determinístico pertence exclusivamente a proveniencia_ia (§2.14.4)"
            )

    return advisories


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
    all_errors = [fmt_schema_error(e) for e in schema_errors] + semantic
    is_valid = not all_errors

    _print_result(path.name, is_valid, expect_valid, all_errors, expected_error)

    if is_valid:
        for advisory in check_ndf_advisories(doc):
            print(f"  {YELLOW}AVISO{RESET}  {path.name}: {advisory}")

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


def _validate_schema_file(path: Path, schema: dict, expect_valid: bool) -> bool:
    raw = json.loads(path.read_text(encoding="utf-8"))
    expected_error = raw.get("_expected_error", "")
    doc = strip_meta(raw)
    errors = [e.message for e in Draft202012Validator(schema).iter_errors(doc)]
    _print_result(path.name, not errors, expect_valid, errors, expected_error)
    return (not errors) == expect_valid


NDT_PATH_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*$")


def check_ndt_semantic(doc: dict) -> list[str]:
    errors = []
    pages = [p.get("id") for p in doc.get("paginas_def", []) if isinstance(p, dict)]
    if len(pages) != len(set(pages)):
        errors.append("paginas_def contém ids duplicados")
    page_ids = set(pages)
    for i, entry in enumerate(doc.get("sequencia", [])):
        if entry.get("pagina_def") not in page_ids:
            errors.append(f"sequencia[{i}].pagina_def referencia página inexistente")

    resources = [r.get("id") for r in doc.get("recursos", []) if isinstance(r, dict)]
    if len(resources) != len(set(resources)):
        errors.append("recursos contém ids duplicados")
    resource_ids = set(resources)

    def walk(value, path=""):
        if isinstance(value, dict):
            for key, child in value.items():
                here = f"{path}.{key}" if path else key
                if key == "referencia_recurso" and child not in resource_ids:
                    errors.append(f"{here} referencia recurso inexistente")
                if key in {"largura", "altura", "tamanho"} and isinstance(child, (int, float)):
                    if child <= 0:
                        errors.append(f"{here} deve ser maior que zero")
                if key in {"referencia", "incluir_se", "fonte_overflow"} and isinstance(child, str):
                    if "{{" not in child and not NDT_PATH_RE.fullmatch(child):
                        errors.append(f"{here} não é um caminho NDF canónico")
                walk(child, here)
        elif isinstance(value, list):
            for i, child in enumerate(value):
                walk(child, f"{path}[{i}]")

    walk(doc)
    return errors


def run_ndt_suite(valid_only=False, invalid_only=False) -> tuple[int, int]:
    schema = _load_schema(NDT_SCHEMA_PATH)
    passed = failed = 0
    print(f"\n{BOLD}{SEP}{RESET}\n{BOLD}NDT — CONFORMIDADE{RESET}\n{SEP}")
    if not invalid_only:
        for valid_dir in (NDT_VALID_DIR, NDT_EXAMPLES_DIR):
            for path in sorted(valid_dir.glob("*.json")):
                raw = json.loads(path.read_text(encoding="utf-8"))
                schema_ok = _validate_schema_file(path, schema, True)
                semantic = check_ndt_semantic(raw)
                if schema_ok and not semantic: passed += 1
                else:
                    if semantic:
                        for error in semantic: print(f"        → {error}")
                    failed += 1
    if not valid_only:
        for path in sorted(NDT_INVALID_DIR.glob("*.json")):
            raw = json.loads(path.read_text(encoding="utf-8"))
            schema_errors = list(Draft202012Validator(schema).iter_errors(strip_meta(raw)))
            semantic = check_ndt_semantic(strip_meta(raw)) if not schema_errors else []
            ok = bool(schema_errors or semantic)
            _print_result(path.name, not ok, False,
                          [e.message for e in schema_errors] + semantic,
                          raw.get("_expected_error", ""))
            if ok: passed += 1
            else: failed += 1
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


def validate_package_dir(root: Path) -> bool:
    """Valida um directório com o conteúdo descomprimido de um .ndfpkg."""
    errors = []
    try:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        core_bytes = (root / "ndf-core.json").read_bytes()
        core = json.loads(core_bytes)
        envelope = json.loads((root / "envelope.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERRO: pacote ilegível — {e}")
        return False

    for name, value, schema_path in (
        ("manifest", manifest, MANIFEST_SCHEMA_PATH),
        ("NDF-core", core, NDF_SCHEMA_PATH),
        ("envelope", envelope, ENVELOPE_SCHEMA_PATH),
    ):
        schema = _load_schema(schema_path)
        for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value):
            errors.append(f"{name}: {fmt_schema_error(e)}")

    # §9.3 (NDF-PKG-007): dentro de um pacote, o schema do tipo resolve-se
    # primeiro a partir de schemas/ — é isso que torna o .ndfpkg autonomamente
    # validável por um terceiro sem acesso ao registo canónico.
    errors.extend(check_ndf_semantic(core, pkg_root=root))

    required_level = core.get("nivel_assinatura")
    signatures = envelope.get("assinaturas") or []
    if required_level in {"avancada", "qualificada"}:
        matching = [s for s in signatures if s.get("nivel") == required_level]
        if not matching:
            errors.append(f"envelope não contém assinatura pessoal {required_level} exigida")
        # timestamps e validation_material são por assinatura (unidade de prova
        # autocontida — SPEC.md §4.4.1), não campos globais do envelope.
        for s in matching:
            if not s.get("timestamps"):
                errors.append(f"assinatura {s.get('assinatura_id', '?')} sem timestamps B-LTA")
            if not s.get("validation_material"):
                errors.append(f"assinatura {s.get('assinatura_id', '?')} sem material de validação")

    items = manifest.get("inventario", [])
    inventory = {item["ficheiro"]: item["hash_sha256"] for item in items}
    if len(inventory) != len(items):
        errors.append("inventário contém nomes de ficheiro duplicados")
    actual_files = {
        str(path.relative_to(root))
        for path in root.rglob("*") if path.is_file()
    } - {"manifest.json", "README.md"}
    unlisted = actual_files - set(inventory)
    if unlisted:
        errors.append("ficheiros não inventariados: " + ", ".join(sorted(unlisted)))
    for rel, declared in inventory.items():
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"inventário: caminho inseguro '{rel}'")
            continue
        target = root / path
        if not target.is_file():
            errors.append(f"inventário: ficheiro ausente '{rel}'")
            continue
        actual = "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != declared:
            errors.append(f"inventário: hash incorrecto para '{rel}'")

    payload_hash = "sha256:" + hashlib.sha256(core_bytes).hexdigest()
    if rfc8785 is not None:
        try:
            canonical = rfc8785.dumps(core)
            if canonical != core_bytes:
                errors.append("ndf-core.json não contém exactamente os bytes JCS/RFC 8785")
        except rfc8785.CanonicalizationError as exc:
            errors.append(f"NDF-core não canonicalizável por RFC 8785: {exc}")
    if envelope.get("payload_hash") != payload_hash or manifest.get("payload_hash") != payload_hash:
        errors.append("payload_hash não corresponde aos bytes de ndf-core.json")

    digest = hashlib.sha256((core.get("ndf_id", "") + "|" + payload_hash).encode("utf-8")).digest()
    code = "NDF-" + base64.b32encode(digest).decode("ascii").rstrip("=")[:20]
    if envelope.get("validation_code") != code or manifest.get("validation_code") != code:
        errors.append("validation_code incorrecto")

    ndt_ref = core.get("ndt_version_ref", "")
    ndt_path = root / "ndt" / f"{ndt_ref}.ndt.json"
    if not ndt_path.is_file():
        errors.append(f"NDT referenciado ausente: {ndt_path.relative_to(root)}")
    else:
        ndt = json.loads(ndt_path.read_text(encoding="utf-8"))
        for e in Draft202012Validator(_load_schema(NDT_SCHEMA_PATH)).iter_errors(ndt):
            errors.append(f"NDT: {e.message}")
        errors.extend(f"NDT: {e}" for e in check_ndt_semantic(ndt))
        expected_ref = f"{ndt.get('schema_id', '')}@{ndt.get('versao_ndt', '')}"
        if expected_ref != ndt_ref:
            errors.append("ndt_version_ref não corresponde à identidade do NDT")

    if errors:
        print(f"{RED}FAIL{RESET}  pacote {root}")
        for e in errors:
            print(f"      → {e}")
        return False
    print(f"{GREEN}PASS{RESET}  pacote {root}")
    for advisory in check_ndf_advisories(core, pkg_root=root):
        print(f"      {YELLOW}AVISO{RESET} {advisory}")
    return True


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="NORMORDIS Conformance Test Runner")
    parser.add_argument("file", nargs="?", type=Path, help="Ficheiro NDF-core a validar.")
    parser.add_argument("--package", type=Path, help="Directório descomprimido de um .ndfpkg a validar.")
    parser.add_argument("--valid-only",   action="store_true")
    parser.add_argument("--invalid-only", action="store_true")
    parser.add_argument("--format", choices=["ndf", "ndt", "ncrtf", "all"], default="all",
                        help="Suite a correr (default: all)")
    args = parser.parse_args()

    if args.package:
        sys.exit(0 if validate_package_dir(args.package) else 1)

    if args.file:
        ok = validate_single(args.file)
        sys.exit(0 if ok else 1)

    p = f = 0
    if args.format in ("ndf", "all"):
        np, nf = run_ndf_suite(args.valid_only, args.invalid_only)
        p += np; f += nf
    if args.format in ("ndt", "all"):
        np, nf = run_ndt_suite(args.valid_only, args.invalid_only)
        p += np; f += nf
    if args.format in ("ncrtf", "all"):
        np, nf = run_ncrtf_suite(args.valid_only, args.invalid_only)
        p += np; f += nf

    _print_total(p, f)
    sys.exit(0 if f == 0 else 1)


if __name__ == "__main__":
    main()
