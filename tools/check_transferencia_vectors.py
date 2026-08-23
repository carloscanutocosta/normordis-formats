#!/usr/bin/env python3
"""Vetores negativos reproduzíveis sobre o conjunto de transferência de exemplo.

«O conjunto está completo» é alegação enquanto não houver caso que a desminta.
Cada mutação abaixo representa uma família de requisito e DEVE ser rejeitada.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from check_transferencia import validate_transfer_dir

try:
    import rfc8785
except ImportError:
    print("ERRO: instale tools/requirements.txt para obter rfc8785", file=sys.stderr)
    raise SystemExit(1)


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "specs/ndf/examples/ndfxfer-example"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _reescreve_declaracao(root: Path, mutacao) -> None:
    """Reescreve transferencia.json e re-sela, para que o caso falhe pela razão
    pretendida e não por o selo ter deixado de bater."""
    path = root / "transferencia.json"
    declaracao = load(path)
    mutacao(declaracao)
    bytes_canonicos = rfc8785.dumps(declaracao)
    path.write_bytes(bytes_canonicos)

    import base64
    payload_hash = "sha256:" + hashlib.sha256(bytes_canonicos).hexdigest()
    bruto = hashlib.sha256(
        f"{declaracao['transferencia_id']}|{payload_hash}".encode("utf-8")).digest()
    envelope_path = root / "transferencia-envelope.json"
    envelope = load(envelope_path)
    envelope["payload_hash"] = payload_hash
    envelope["validation_code"] = "NDF-" + base64.b32encode(bruto).decode("ascii").rstrip("=")[:20]
    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")


def _evidencia_com_omissoes(root: Path) -> Path:
    """A evidência que retém eventos — a posição na ordenação não é critério."""
    for path in sorted((root / "evidencia").glob("*.json")):
        if load(path).get("omitidos", {}).get("contagem", 0) > 0:
            return path
    raise RuntimeError("nenhuma evidência com omissões no conjunto de exemplo")


def _evidencia_completa(root: Path) -> Path:
    """A evidência que transfere a cadeia integral."""
    for path in sorted((root / "evidencia").glob("*.json")):
        if load(path).get("omitidos", {}).get("contagem", 0) == 0:
            return path
    raise RuntimeError("nenhuma evidência integral no conjunto de exemplo")


def _unidade_ausente(root: Path) -> None:
    """Unidade declarada mas não presente: o conjunto chega incompleto."""
    declaracao = load(root / "transferencia.json")
    shutil.rmtree(root / declaracao["unidades"][0]["ficheiro"])


def _unidade_a_mais(root: Path) -> None:
    """Pacote presente e não declarado: foi acrescentado, e o selo não o cobre."""
    declaracao = load(root / "transferencia.json")
    origem = root / declaracao["unidades"][0]["ficheiro"]
    shutil.copytree(origem, root / "unidades/clandestino.ndfpkg")


def _payload_hash_divergente(root: Path) -> None:
    """Substituir a unidade por outra versão do mesmo documento.

    O ndf_id continua a bater; só o payload_hash denuncia — que é a razão de a
    declaração o exigir, como já fazem as relações documentais.
    """
    def mutacao(d):
        d["unidades"][0]["payload_hash"] = "sha256:" + "0" * 64
    _reescreve_declaracao(root, mutacao)


def _selo_ausente(root: Path) -> None:
    """Sem selo, a declaração de composição é afirmação de ninguém."""
    (root / "transferencia-envelope.json").unlink()


def _selo_nao_cobre(root: Path) -> None:
    """Declaração alterada depois de selada: o fundamento muda, o selo não."""
    path = root / "transferencia.json"
    declaracao = load(path)
    declaracao["fundamento"] = "Fundamento substituído após a selagem."
    path.write_bytes(rfc8785.dumps(declaracao))


def _referencia_externa_omitida(root: Path) -> None:
    """O conjunto não fecha e não o declara — D-XFER-1."""
    _reescreve_declaracao(root, lambda d: d.__setitem__("referencias_externas", []))


def _referencia_externa_inventada(root: Path) -> None:
    """Declara como externa uma relação cujo alvo está no conjunto.

    Sentido inverso da mesma regra: a lista é derivada, logo tão verificável
    contra o excesso como contra a falta.
    """
    def mutacao(d):
        d["referencias_externas"].append({
            "declarada_por": d["unidades"][0]["ndf_id"],
            "tipo": "referencia",
            "alvo": {
                "ndf_id": d["unidades"][1]["ndf_id"],
                "payload_hash": d["unidades"][1]["payload_hash"],
            },
        })
    _reescreve_declaracao(root, mutacao)


def _evidencia_contagem_nao_fecha(root: Path) -> None:
    """Eventos transferidos + omitidos ≠ total: a aritmética denuncia."""
    path = _evidencia_com_omissoes(root)
    ev = load(path)
    ev["omitidos"]["contagem"] = 0
    path.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _evidencia_evento_editado(root: Path) -> None:
    """Evento com o conteúdo alterado e o event_hash mantido — CUST-REQ-004."""
    path = _evidencia_com_omissoes(root)
    ev = load(path)
    ev["eventos"][0]["occurred_at"] = "2020-01-01T00:00:00Z"
    path.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _evidencia_fora_da_politica(root: Path) -> None:
    """Evento transferido que a política declarada não prevê — D-XFER-2.

    É o que revela selecção caso a caso em vez de política aplicada.
    """
    path = _evidencia_com_omissoes(root)
    ev = load(path)
    ev["politica_extracao"]["tipos"] = ["finalizado"]
    path.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _evidencia_sem_finalizado_na_politica(root: Path) -> None:
    """Política que exclui 'finalizado': o extrato deixa de estabelecer quando o
    documento se tornou imutável, e não é evidência de custódia."""
    path = _evidencia_completa(root)
    ev = load(path)
    ev["politica_extracao"]["tipos"] = [t for t in ev["politica_extracao"]["tipos"]
                                        if t != "finalizado"]
    path.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CASOS = [
    ("XFER-NEG-001-unidade-ausente", _unidade_ausente),
    ("XFER-NEG-002-unidade-a-mais", _unidade_a_mais),
    ("XFER-NEG-003-payload-hash-divergente", _payload_hash_divergente),
    ("XFER-NEG-004-selo-ausente", _selo_ausente),
    ("XFER-NEG-005-selo-nao-cobre", _selo_nao_cobre),
    ("XFER-NEG-006-referencia-externa-omitida", _referencia_externa_omitida),
    ("XFER-NEG-007-referencia-externa-inventada", _referencia_externa_inventada),
    ("XFER-NEG-008-evidencia-contagem-nao-fecha", _evidencia_contagem_nao_fecha),
    ("XFER-NEG-009-evidencia-evento-editado", _evidencia_evento_editado),
    ("XFER-NEG-010-evidencia-fora-da-politica", _evidencia_fora_da_politica),
    ("XFER-NEG-011-politica-sem-finalizado", _evidencia_sem_finalizado_na_politica),
]


def main() -> int:
    if not (SOURCE / "unidades").is_dir():
        subprocess.run([sys.executable, str(ROOT / "tools/build_ndfxfer_example.py")],
                       check=True, capture_output=True)
    if not validate_transfer_dir(SOURCE):
        print("FAIL baseline do conjunto de transferência")
        return 1
    falhados = 0
    with tempfile.TemporaryDirectory(prefix="normordis-xfer-") as tmp:
        for nome, mutar in CASOS:
            alvo = Path(tmp) / nome
            shutil.copytree(SOURCE, alvo)
            mutar(alvo)
            if validate_transfer_dir(alvo):
                print(f"FAIL {nome}: conjunto inválido foi aceite")
                falhados += 1
            else:
                print(f"PASS {nome}: rejeitado como esperado")
    print(f"PASS transfer vectors: {len(CASOS) - falhados}/{len(CASOS)}"
          if not falhados else f"FAIL transfer vectors: {falhados}")
    return 1 if falhados else 0


if __name__ == "__main__":
    raise SystemExit(main())
