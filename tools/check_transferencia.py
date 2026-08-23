#!/usr/bin/env python3
"""Valida um conjunto de transferência (.ndfxfer) materializado como diretório.

Verifica o que um recetor consegue verificar tendo apenas o que recebeu em mãos
— que é o critério que decide o que pode ser conformidade (ADR-022, ADR-024).
Não aprecia se o fundamento invocado é bastante, se o destinatário devia aceitar,
nem se a política de extração é adequada: isso é do transmitente e do arquivo.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

try:
    import rfc8785
except ImportError:
    print("ERRO: instale tools/requirements.txt para obter rfc8785", file=sys.stderr)
    raise SystemExit(1)


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_XFER = ROOT / "specs/ndf/schemas/transferencia.schema.json"
SCHEMA_EVID = ROOT / "specs/ndf/schemas/evidencia-custodia.schema.json"
SCHEMA_EVENTO = ROOT / "specs/ndf/schemas/custody-event.schema.json"

GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(dados: bytes) -> str:
    return "sha256:" + hashlib.sha256(dados).hexdigest()


def _validar_declaracao(root: Path, erros: list[str]) -> dict | None:
    path = root / "transferencia.json"
    if not path.is_file():
        erros.append("transferencia.json ausente")
        return None
    bruto = path.read_bytes()
    declaracao = json.loads(bruto.decode("utf-8"))
    validador = Draft202012Validator(load(SCHEMA_XFER), format_checker=FormatChecker())
    for e in validador.iter_errors(declaracao):
        erros.append(f"transferencia.json: {e.message} (campo: {'/'.join(str(p) for p in e.absolute_path)})")
    if rfc8785.dumps(declaracao) != bruto:
        erros.append("transferencia.json não contém exactamente os bytes JCS/RFC 8785")
    return declaracao


def _validar_selo(root: Path, declaracao: dict, erros: list[str]) -> None:
    """O selo prende a declaração de composição a quem a fez.

    Sem ele, «este conjunto é composto por estas unidades» é afirmação de
    ninguém — e a composição é precisamente o que o conjunto acrescenta.
    """
    path = root / "transferencia-envelope.json"
    if not path.is_file():
        erros.append("transferencia-envelope.json ausente: a declaração de composição não está selada")
        return
    envelope = load(path)
    esperado = digest((root / "transferencia.json").read_bytes())
    if envelope.get("payload_hash") != esperado:
        erros.append("selo: payload_hash não corresponde aos bytes de transferencia.json")
    bruto = hashlib.sha256(
        f"{declaracao.get('transferencia_id', '')}|{esperado}".encode("utf-8")).digest()
    import base64
    codigo = "NDF-" + base64.b32encode(bruto).decode("ascii").rstrip("=")[:20]
    if envelope.get("validation_code") != codigo:
        erros.append("selo: validation_code incorrecto")


def _resolver_unidade(root: Path, ficheiro: str) -> Path | None:
    """A unidade é um .ndfpkg; o repositório guarda-o na forma desempacotada."""
    alvo = root / ficheiro
    if alvo.is_dir() and (alvo / "ndf-core.json").is_file():
        return alvo
    return None


def _validar_unidades(root: Path, declaracao: dict, erros: list[str]) -> dict[str, dict]:
    """Fecho nos dois sentidos, na forma de NDF-PKG-009 elevada ao conjunto."""
    cores: dict[str, dict] = {}
    declarados_ficheiro = set()
    for unidade in declaracao.get("unidades", []):
        ficheiro = unidade.get("ficheiro", "")
        declarados_ficheiro.add(ficheiro)
        pacote = _resolver_unidade(root, ficheiro)
        if pacote is None:
            erros.append(f"unidade '{ficheiro}' declarada mas ausente do conjunto")
            continue
        bytes_core = (pacote / "ndf-core.json").read_bytes()
        core = json.loads(bytes_core.decode("utf-8"))
        cores[core.get("ndf_id", "")] = core
        if core.get("ndf_id") != unidade.get("ndf_id"):
            erros.append(f"unidade '{ficheiro}': ndf_id do pacote não corresponde ao declarado")
        real = digest(bytes_core)
        if real != unidade.get("payload_hash"):
            erros.append(
                f"unidade '{ficheiro}': payload_hash declarado não corresponde ao NDF-core "
                f"— a declaração não prende a versão exata")
        manifest = pacote / "manifest.json"
        if manifest.is_file() and load(manifest).get("validation_code") != unidade.get("validation_code"):
            erros.append(f"unidade '{ficheiro}': validation_code não corresponde ao do pacote")

    # Sentido inverso: um pacote presente e não declarado foi acrescentado por
    # alguém, e o selo do transmitente não o cobre.
    pasta = root / "unidades"
    if pasta.is_dir():
        for candidato in sorted(pasta.iterdir()):
            if not (candidato.is_dir() and (candidato / "ndf-core.json").is_file()):
                continue
            rel = candidato.relative_to(root).as_posix()
            if rel not in declarados_ficheiro:
                erros.append(f"'{rel}' está no conjunto mas não consta de unidades[]")
    return cores


def _validar_referencias_externas(declaracao: dict, cores: dict, erros: list[str]) -> None:
    """D-XFER-1: é informação derivada, logo recomputável e verificável."""
    presentes = set(cores)
    esperado = []
    for ndf_id, core in sorted(cores.items()):
        for relacao in core.get("relacoes", []) or []:
            alvo = relacao.get("alvo", {})
            if alvo.get("ndf_id") in presentes:
                continue
            esperado.append((ndf_id, relacao.get("tipo"),
                             alvo.get("ndf_id"), alvo.get("payload_hash")))
    declarado = [
        (r.get("declarada_por"), r.get("tipo"),
         r.get("alvo", {}).get("ndf_id"), r.get("alvo", {}).get("payload_hash"))
        for r in declaracao.get("referencias_externas", [])
    ]
    for extra in sorted(set(declarado) - set(esperado)):
        erros.append(
            f"referencias_externas declara {extra[1]} → {extra[2]} que não resulta das "
            f"unidades recebidas (alvo presente no conjunto, ou relação inexistente)")
    for falta in sorted(set(esperado) - set(declarado)):
        erros.append(
            f"referencias_externas omite {falta[1]} → {falta[2]}, declarada por "
            f"{falta[0]}: o conjunto não fecha e não o declara")


def _validar_inventario(root: Path, declaracao: dict, erros: list[str]) -> None:
    for item in declaracao.get("inventario", []):
        alvo = root / item.get("ficheiro", "")
        if not alvo.is_file():
            erros.append(f"inventário: ficheiro ausente '{item.get('ficheiro')}'")
            continue
        if digest(alvo.read_bytes()) != item.get("hash_sha256"):
            erros.append(f"inventário: hash incorrecto para '{item.get('ficheiro')}'")


def _validar_evidencia(root: Path, cores: dict, erros: list[str]) -> None:
    pasta = root / "evidencia"
    if not pasta.is_dir():
        return
    schema = Draft202012Validator(load(SCHEMA_EVID), format_checker=FormatChecker())
    schema_evento = Draft202012Validator(load(SCHEMA_EVENTO), format_checker=FormatChecker())
    for path in sorted(pasta.glob("*.json")):
        ev = load(path)
        nome = path.name
        for e in schema.iter_errors(ev):
            erros.append(f"{nome}: {e.message}")
        eventos = ev.get("eventos", [])
        if not isinstance(eventos, list):
            continue

        for i, evento in enumerate(eventos):
            for e in schema_evento.iter_errors(evento):
                erros.append(f"{nome}: evento {i}: {e.message}")
            # Íntegro e não editado (CUST-REQ-004): o hash recomputa a partir do
            # próprio evento, e é o que o recetor consegue verificar sozinho.
            sem = {k: v for k, v in evento.items() if k != "event_hash"}
            real = "sha256:" + hashlib.sha256(rfc8785.dumps(sem)).hexdigest()
            if evento.get("event_hash") != real:
                erros.append(f"{nome}: evento {i}: event_hash incorrecto — evento editado")
            if evento.get("ndf_id") != ev.get("ndf_id"):
                erros.append(f"{nome}: evento {i}: ndf_id não corresponde ao da evidência")

        sequencias = [e.get("sequence") for e in eventos if isinstance(e, dict)]
        if sequencias != sorted(sequencias) or len(set(sequencias)) != len(sequencias):
            erros.append(f"{nome}: eventos fora de ordem ou com sequence repetida")

        total = ev.get("cadeia", {}).get("eventos_total")
        omitidos = ev.get("omitidos", {}).get("contagem")
        if isinstance(total, int) and isinstance(omitidos, int) and len(eventos) + omitidos != total:
            erros.append(
                f"{nome}: {len(eventos)} transferidos + {omitidos} omitidos ≠ {total} declarados "
                f"— a contagem não fecha")

        # D-XFER-2 regra 1: a política é declarada e aplicada, não uma seleção
        # caso a caso. Um evento fora da política revela selecção manual.
        tipos = set(ev.get("politica_extracao", {}).get("tipos", []))
        for evento in eventos:
            if isinstance(evento, dict) and evento.get("event_type") not in tipos:
                erros.append(
                    f"{nome}: evento de tipo '{evento.get('event_type')}' fora da política "
                    f"declarada '{ev.get('politica_extracao', {}).get('id')}'")

        if ev.get("ndf_id") not in cores:
            erros.append(f"{nome}: evidência para uma unidade que não faz parte do conjunto")


def validate_transfer_dir(root: Path) -> bool:
    erros: list[str] = []
    declaracao = _validar_declaracao(root, erros)
    if declaracao is not None:
        _validar_selo(root, declaracao, erros)
        cores = _validar_unidades(root, declaracao, erros)
        _validar_referencias_externas(declaracao, cores, erros)
        _validar_inventario(root, declaracao, erros)
        _validar_evidencia(root, cores, erros)
    if erros:
        print(f"  {RED}FAIL{RESET}  conjunto {root}")
        for e in erros[:12]:
            print(f"        → {e}")
        return False
    print(f"  {GREEN}PASS{RESET}  conjunto {root}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("conjunto", type=Path, nargs="+")
    args = parser.parse_args()
    return 0 if all(validate_transfer_dir(c) for c in args.conjunto) else 1


if __name__ == "__main__":
    raise SystemExit(main())
