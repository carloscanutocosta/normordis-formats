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
  C6  schemas embebidos nos pacotes de exemplo são idênticos ao canónico
  C7  `componentes` é o mesmo vocabulário em todos os schemas de tipo
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

# C1/C2 para as especificações cujos blocos JSON são fragmentos de um documento
# maior — um elemento gráfico, um nó de texto — e não documentos completos.
FRAGMENT_SPECS = {
    "ndt": {
        "spec": ROOT / "specs/ndt/SPEC.md",
        "schema": ROOT / "specs/ndt/schemas/ndt.schema.json",
        "discriminante": "tipo",
    },
    "ncrtf": {
        "spec": ROOT / "specs/ncrtf/SPEC.md",
        "schema": ROOT / "specs/ncrtf/schemas/ncrtf.schema.json",
        "discriminante": "type",
    },
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


def defs_por_discriminante(schema: dict, discriminante: str) -> dict[str, list[str]]:
    """Mapeia o valor do discriminante para os `$defs` que o declaram.

    Um mesmo valor pode pertencer a vários contextos — `imagem` existe como
    elemento gráfico e como elemento de fluxo — pelo que o valor é uma lista.
    """
    encontrados: dict[str, list[str]] = {}
    for nome, definicao in schema.get("$defs", {}).items():
        propriedade = definicao.get("properties", {}).get(discriminante, {})
        if isinstance(propriedade, dict):
            const = propriedade.get("const")
            if isinstance(const, str):
                encontrados.setdefault(const, []).append(nome)
    return encontrados


def c1_fragment_blocks(failures) -> int:
    """C1 para fragmentos: cada bloco JSON discriminado valida contra o `$def`.

    Um bloco cujo discriminante admita vários contextos é aceite se validar
    contra pelo menos um deles — a SPEC ilustra ora um, ora outro.
    """
    checked = 0
    for nome, cfg in FRAGMENT_SPECS.items():
        schema = load(cfg["schema"])
        candidatos = defs_por_discriminante(schema, cfg["discriminante"])
        texto = cfg["spec"].read_text(encoding="utf-8")
        for start, sec, obj in json_blocks(texto):
            if not isinstance(obj, dict):
                continue
            valor = obj.get(cfg["discriminante"])
            if not isinstance(valor, str) or valor not in candidatos:
                continue
            checked += 1
            motivos = []
            for def_name in candidatos[valor]:
                fragmento = dict(schema)
                fragmento.pop("$defs", None)
                validador = Draft202012Validator(
                    {**schema["$defs"][def_name], "$defs": schema["$defs"]},
                    format_checker=FormatChecker(),
                )
                erros = [e.message for e in validador.iter_errors(obj)]
                if not erros:
                    motivos = []
                    break
                motivos.append(f"{def_name}: {erros[0]}")
            if motivos:
                failures.append(
                    f"C1 {cfg['spec'].relative_to(ROOT)} §{sec} (linha {start}): "
                    f"bloco `{valor}` não valida contra nenhum $def — "
                    + " | ".join(motivos)
                )
    return checked


def c2_fragment_fields(failures) -> int:
    """C2 para as SPEC de fragmentos: campo no schema, ausente da SPEC."""
    checked = 0
    for nome, cfg in FRAGMENT_SPECS.items():
        schema = load(cfg["schema"])
        texto = cfg["spec"].read_text(encoding="utf-8")
        for field in sorted(schema_properties(schema)):
            if field in DOCUMENTATION_EXEMPT:
                continue
            checked += 1
            if f"`{field}`" not in texto and f'"{field}"' not in texto:
                failures.append(
                    f"C2 {cfg['schema'].relative_to(ROOT)} declara `{field}`, "
                    f"que nunca é mencionado em {cfg['spec'].relative_to(ROOT)}"
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


def c6_embedded_schema_copies(failures):
    """Um pacote transporta os schemas para ser verificável sem rede.

    Uma cópia que divirja do canónico declara o mesmo `$id` e valida coisas
    diferentes: um verificador que resolva o schema a partir do pacote — que é o
    que o pacote existe para permitir — obtém outro contrato. Foi assim que três
    pacotes ficaram com um `ndf-core.schema.json` anterior a ADR-023, rejeitando
    `origem_nao_identificavel` enquanto a SPEC o documentava.
    """
    canonicos = {
        "ndf-core.schema.json": ROOT / "specs/ndf/schemas/ndf-core.schema.json",
        "envelope.schema.json": ROOT / "specs/ndf/schemas/envelope.schema.json",
        "manifest.schema.json": ROOT / "specs/ndf/schemas/manifest.schema.json",
        "custody-event.schema.json": ROOT / "specs/ndf/schemas/custody-event.schema.json",
        "ndt.schema.json": ROOT / "specs/ndt/schemas/ndt.schema.json",
        "ncrtf.schema.json": ROOT / "specs/ncrtf/schemas/ncrtf.schema.json",
    }
    for pasta in sorted((ROOT / "specs/ndf/examples").glob("*/schemas")):
        for copia in sorted(pasta.glob("*.json")):
            canon = canonicos.get(copia.name)
            if canon is None:
                # schema de tipo ou de perfil: procura-se no registo
                for base in ("specs/registry/schemas", "specs/registry/profiles"):
                    alvo = ROOT / base / copia.name
                    if alvo.is_file():
                        canon = alvo
                        break
            if canon is None:
                continue
            if load(copia) != load(canon):
                failures.append(
                    f"C6 {copia.relative_to(ROOT)} diverge de "
                    f"{canon.relative_to(ROOT)} — mesmo $id, contrato diferente"
                )
    return len(canonicos)


def c7_componentes_vocabulary(failures):
    """`componentes` é o mecanismo único de binários (SPEC §2.8.1).

    Os schemas de tipo são autocontidos por desenho — um pacote transporta um e
    tem de o validar sem rede —, pelo que a definição é necessariamente
    duplicada. Duplicação sem guarda deriva: foi assim que `oficio` ficou com um
    `anexos[]` próprio, com outros nomes de campo e sem `media_type`, que
    `NDF-PKG-009` não reconhecia — um ofício não conseguia transportar os seus
    anexos num pacote conforme.

    Verifica-se a forma dos itens, não a cardinalidade: `documento-capturado`
    exige pelo menos um componente, um tipo nativo não.
    """
    base = ROOT / "specs/registry/schemas/documento-capturado.schema.json"
    if not base.is_file():
        return 0
    canonico = load(base)["properties"]["componentes"]["items"]
    verificados = 0
    for schema_path in sorted((ROOT / "specs/registry/schemas").glob("*.schema.json")):
        if schema_path == base:
            continue
        comp = load(schema_path).get("properties", {}).get("componentes")
        if comp is None:
            # um tipo sem componentes é legítimo; o que não é legítimo é ter
            # outro vocabulário para o mesmo fim
            props = load(schema_path).get("properties", {})
            for suspeito in ("anexos", "ficheiros", "documentos_anexos"):
                if suspeito in props:
                    failures.append(
                        f"C7 {schema_path.relative_to(ROOT)} define `{suspeito}` — "
                        f"o mecanismo de componentes binários é `componentes` (SPEC §2.8.1)"
                    )
            continue
        verificados += 1
        if comp.get("items") != canonico:
            failures.append(
                f"C7 {schema_path.relative_to(ROOT)}: `componentes.items` diverge da "
                f"definição de {base.relative_to(ROOT)}"
            )
    return verificados


def main() -> int:
    schemas = {n: load(p) for n, p in SCHEMAS.items()}
    failures: list[str] = []

    n1 = c1_spec_blocks(schemas, failures) + c1_fragment_blocks(failures)
    n2 = c2_documented_fields(schemas, failures) + c2_fragment_fields(failures)
    n3 = c3_section_refs(failures)
    n4 = c4_duplicated_enums(schemas, failures)
    n5 = c5_removed_properties(failures)
    n6 = c6_embedded_schema_copies(failures)
    n7 = c7_componentes_vocabulary(failures)

    if failures:
        for f in failures:
            print(f"FAIL {f}")
        print(f"\nFAIL spec coherence: {len(failures)} problemas")
        return 1

    print(
        f"PASS spec coherence: {n1} blocos JSON, {n2} campos de schema, "
        f"{n3} referências de secção, {n4} enums duplicados, "
        f"{n5} propriedades removidas, {n6} schemas verificados nas cópias, "
        f"{n7} tipos com componentes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
