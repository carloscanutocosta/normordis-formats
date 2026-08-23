#!/usr/bin/env python3
"""Executa vetores negativos reproduzíveis sobre o exemplo .ndfpkg."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from validate import validate_package_dir


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "specs/ndf/examples/ndfpkg-example"
SOURCE_CAPTURA = ROOT / "specs/ndf/examples/captura-requerimento"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_inventory_hash(root: Path, relative: str) -> None:
    manifest_path = root / "manifest.json"
    manifest = load(manifest_path)
    digest = "sha256:" + hashlib.sha256((root / relative).read_bytes()).hexdigest()
    for item in manifest["inventario"]:
        if item["ficheiro"] == relative:
            item["hash_sha256"] = digest
            dump(manifest_path, manifest)
            return
    raise RuntimeError(f"entrada ausente no inventário: {relative}")


def cases(root: Path):
    yield "PKG-NEG-001-hash-alterado", lambda p: _tamper_hash(p)
    yield "PKG-NEG-002-ficheiro-nao-inventariado", lambda p: (p / "extra.bin").write_bytes(b"x")
    yield "PKG-NEG-003-inventario-duplicado", lambda p: _duplicate_item(p)
    yield "PKG-NEG-004-caminho-inseguro", lambda p: _unsafe_path(p)
    yield "PKG-NEG-005-ndt-ausente", lambda p: (p / "ndt/oficio-generico@2.0.0.ndt.json").unlink()
    yield "PKG-NEG-006-identidade-ndt-divergente", lambda p: _mismatch_ndt(p)
    yield "PKG-NEG-007-envelope-sem-timestamps", lambda p: _remove_timestamps(p)
    yield "PKG-NEG-008-assinatura-sem-id", lambda p: _remove_assinatura_id(p)
    yield "PKG-NEG-009-ndt-referencia-pendurada", lambda p: _dangling_ndt_ref(p)
    yield "PKG-NEG-015-anexo-nativo-ausente", lambda p: _anexo_nativo_ausente(p)
    yield "PKG-NEG-016-anexo-nativo-nao-declarado", lambda p: _anexo_nativo_nao_declarado(p)


def cases_captura(root: Path):
    """Vetores próprios do documento capturado (§2.8.1, NDF-PKG-009)."""
    yield "PKG-NEG-010-componente-ausente-do-pacote", lambda p: _componente_ausente(p)
    yield "PKG-NEG-011-digest-divergente", lambda p: _digest_divergente(p)
    yield "PKG-NEG-012-ficheiro-nao-declarado", lambda p: _ficheiro_nao_declarado(p)
    yield "PKG-NEG-013-original-reescrito", lambda p: _original_reescrito(p)
    yield "PKG-NEG-014-sem-estado-reconstituicao", lambda p: _sem_reconstituicao(p)


def _caminho_componente(root: Path) -> Path:
    return root / "original/requerimento.pdf"


def _componente_ausente(root: Path) -> None:
    """Componente declarado no NDF-core mas ausente do pacote materializado.

    Remove-se também do inventário, para provar NDF-PKG-009 e não apenas a
    regra genérica de ficheiro inventariado em falta.
    """
    alvo = _caminho_componente(root)
    digest = "sha256:" + hashlib.sha256(alvo.read_bytes()).hexdigest()
    alvo.unlink()
    manifest_path = root / "manifest.json"
    manifest = load(manifest_path)
    manifest["inventario"] = [
        i for i in manifest["inventario"] if i["hash_sha256"] != digest
    ]
    dump(manifest_path, manifest)


def _digest_divergente(root: Path) -> None:
    """Bytes do componente alterados; inventário atualizado, NDF-core não.

    É o ataque que motivou ADR-021: sem NDF-PKG-009, o pacote passaria — a
    assinatura cobre o NDF-core, e o manifesto não é assinado.
    """
    alvo = _caminho_componente(root)
    alvo.write_bytes(alvo.read_bytes() + b"% adulterado\n")
    update_inventory_hash(root, "original/requerimento.pdf")


def _ficheiro_nao_declarado(root: Path) -> None:
    """Ficheiro em original/ inventariado mas não declarado como componente."""
    extra = root / "original/nao-declarado.pdf"
    extra.write_bytes(b"%PDF-1.4\n% componente clandestino\n%%EOF\n")
    manifest_path = root / "manifest.json"
    manifest = load(manifest_path)
    manifest["inventario"].append({
        "ficheiro": "original/nao-declarado.pdf",
        "hash_sha256": "sha256:" + hashlib.sha256(extra.read_bytes()).hexdigest(),
    })
    dump(manifest_path, manifest)


def _original_reescrito(root: Path) -> None:
    """Original reescrito e o NDF-core 'harmonizado' com os novos bytes.

    Viola NDF-PROD-020: o digest passa a bater, mas payload_hash deixa de
    corresponder aos bytes de ndf-core.json. Um original preservado não se
    reescreve — reescrevê-lo obriga a um NDF novo.
    """
    alvo = _caminho_componente(root)
    novos = alvo.read_bytes().replace(b"Requerimento", b"Reqverimento")
    alvo.write_bytes(novos)
    digest = "sha256:" + hashlib.sha256(novos).hexdigest()
    core_path = root / "ndf-core.json"
    core = load(core_path)
    core["documento"]["componentes"][0]["sha256"] = digest
    core["documento"]["componentes"][0]["tamanho"] = len(novos)
    dump(core_path, core)
    update_inventory_hash(root, "original/requerimento.pdf")
    update_inventory_hash(root, "ndf-core.json")


def _sem_reconstituicao(root: Path) -> None:
    """Documento capturado sem estado de reconstituição declarado.

    A ausência de estratégia tem de ser representável e visível (ADR-022);
    omitir o bloco não é forma de a declarar.
    """
    core_path = root / "ndf-core.json"
    core = load(core_path)
    del core["documento"]["reconstituicao"]
    dump(core_path, core)
    update_inventory_hash(root, "ndf-core.json")


def _dangling_ndt_ref(root: Path) -> None:
    """Acrescenta ao NDT um campo que liga a um caminho impossível no tipo.

    'oficio.schema.json' tem additionalProperties: false, logo nenhum ofício
    conforme pode ter 'campo_inexistente' — o NDT fica irrenderizável e isso
    DEVE ser detectado sem depender de instância.
    """
    ndt_path = next((root / "ndt").glob("*.ndt.json"))
    ndt = load(ndt_path)
    ndt["paginas_def"][0].setdefault("campos", []).append({
        "referencia": "campo_inexistente.subcampo",
        "posicao": {"x": 10, "y": 10},
        "largura": 50,
        "altura": 6,
    })
    dump(ndt_path, ndt)
    update_inventory_hash(root, str(ndt_path.relative_to(root)))


def _tamper_hash(root: Path) -> None:
    manifest = load(root / "manifest.json")
    manifest["inventario"][0]["hash_sha256"] = "sha256:" + "0" * 64
    dump(root / "manifest.json", manifest)


def _duplicate_item(root: Path) -> None:
    manifest = load(root / "manifest.json")
    manifest["inventario"].append(dict(manifest["inventario"][0]))
    dump(root / "manifest.json", manifest)


def _unsafe_path(root: Path) -> None:
    manifest = load(root / "manifest.json")
    manifest["inventario"].append({
        "ficheiro": "../escape.json",
        "hash_sha256": "sha256:" + "0" * 64,
    })
    dump(root / "manifest.json", manifest)


def _mismatch_ndt(root: Path) -> None:
    relative = "ndt/oficio-generico@2.0.0.ndt.json"
    path = root / relative
    ndt = load(path)
    ndt["schema_id"] = "outro-template"
    dump(path, ndt)
    update_inventory_hash(root, relative)


def _remove_timestamps(root: Path) -> None:
    # timestamps é por assinatura (unidade de prova autocontida — SPEC.md
    # §4.4.1), não um campo global do envelope.
    relative = "envelope.json"
    path = root / relative
    envelope = load(path)
    for assinatura in envelope.get("assinaturas", []):
        assinatura.pop("timestamps", None)
    dump(path, envelope)
    update_inventory_hash(root, relative)


def _remove_assinatura_id(root: Path) -> None:
    # Cada assinatura é uma unidade de prova autocontida (ADR-004) —
    # assinatura_id é obrigatório para referenciação inequívoca.
    relative = "envelope.json"
    path = root / relative
    envelope = load(path)
    for assinatura in envelope.get("assinaturas", []):
        assinatura.pop("assinatura_id", None)
    dump(path, envelope)
    update_inventory_hash(root, relative)


def _anexo_nativo_ausente(root: Path) -> None:
    """Anexo de documento nativo declarado no NDF-core mas ausente do pacote.

    Mesma regra de NDF-PKG-009 aplicada à via nativa: um ofício que declara um
    anexo e não o transporta chega incompleto ao destinatário. Antes de §2.8.1.3
    este caso passava, porque o vocabulário `anexos[]` do schema do ofício não
    era reconhecido pelo fecho de pacote.
    """
    alvo = root / "anexos/mapa-medicoes.txt"
    digest = "sha256:" + hashlib.sha256(alvo.read_bytes()).hexdigest()
    alvo.unlink()
    manifest_path = root / "manifest.json"
    manifest = load(manifest_path)
    manifest["inventario"] = [
        i for i in manifest["inventario"] if i["hash_sha256"] != digest
    ]
    dump(manifest_path, manifest)


def _anexo_nativo_nao_declarado(root: Path) -> None:
    """Ficheiro em anexos/ inventariado mas não declarado como componente.

    Sentido inverso do fecho: estar inventariado garante integridade, não
    estatuto documental — a assinatura não cobre o que não foi declarado.
    """
    extra = root / "anexos/clandestino.txt"
    extra.write_bytes(b"anexo que ninguem declarou\n")
    manifest_path = root / "manifest.json"
    manifest = load(manifest_path)
    manifest["inventario"].append({
        "ficheiro": "anexos/clandestino.txt",
        "hash_sha256": "sha256:" + hashlib.sha256(extra.read_bytes()).hexdigest(),
    })
    dump(manifest_path, manifest)


def main() -> int:
    for origem, rotulo in ((SOURCE, "package"), (SOURCE_CAPTURA, "captura")):
        if not validate_package_dir(origem):
            print(f"FAIL {rotulo} baseline")
            return 1
    failed = total = 0
    with tempfile.TemporaryDirectory(prefix="normordis-package-") as tmp:
        base = Path(tmp)
        for origem, gerador in ((SOURCE, cases), (SOURCE_CAPTURA, cases_captura)):
            for name, mutate in gerador(base):
                total += 1
                target = base / name
                shutil.copytree(origem, target)
                mutate(target)
                if validate_package_dir(target):
                    print(f"FAIL {name}: pacote inválido foi aceite")
                    failed += 1
                else:
                    print(f"PASS {name}: rejeitado como esperado")
    print(f"PASS package vectors: {total - failed}/{total}" if not failed else f"FAIL package vectors: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
