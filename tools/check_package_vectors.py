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
    yield "PKG-NEG-017-ndt-texto-alterado-manifesto-recalculado", lambda p: _ndt_texto_alterado_manifesto_recalculado(p)
    yield "PKG-NEG-018-schema-perfil-trocado-manifesto-recalculado", lambda p: _schema_trocado_manifesto_recalculado(p)
    yield "PKG-NEG-019-dependencia-omitida", lambda p: _dependencia_omitida(p)
    yield "PKG-NEG-020-schema-canonico-trocado-manifesto-recalculado", lambda p: _schema_canonico_trocado(p)
    yield "PKG-NEG-021-recurso-trocado-manifesto-recalculado", lambda p: _recurso_trocado(p)
    yield "PKG-NEG-022-recurso-candidatos-ambiguos", lambda p: _recurso_candidatos_ambiguos(p)


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


def _ndt_texto_alterado_manifesto_recalculado(root: Path) -> None:
    """Reproduz o achado externo R16: altera texto fixo do NDT e recalcula
    apenas o hash físico em manifest.json, sem tocar em ndf-core.json.

    Antes de ADR-026 (`dependencias_interpretacao`), isto passava — o hash do
    NDT só existia no manifesto, fora dos bytes assinados. `schema_id` e
    `versao_ndt` mantêm-se inalterados; só o conteúdo visível muda. A
    verificação que tem de apanhar isto é NDF-PKG-010/NDF-READ-025 — a
    entrada 'ndt' de `dependencias_interpretacao` (dentro do NDF-core, logo
    dos bytes assinados) fica desatualizada, e o pacote deixa de fechar.
    """
    relative = "ndt/oficio-generico@2.0.0.ndt.json"
    path = root / relative
    ndt = load(path)
    elementos = ndt["paginas_def"][0]["fluxo"]["elementos"]
    for elemento in elementos:
        if elemento.get("tipo") == "texto_fixo":
            elemento["conteudo"] = "PEDIDO INDEFERIDO — texto alterado no template"
            break
    else:
        raise RuntimeError("nenhum texto_fixo encontrado no NDT de exemplo")
    dump(path, ndt)
    update_inventory_hash(root, relative)
    # ndf-core.json (e dependencias_interpretacao) ficam intencionalmente
    # desatualizados — é exactamente isso que a verificação tem de apanhar.


def _schema_trocado_manifesto_recalculado(root: Path) -> None:
    """Troca o schema do perfil de avaliação mantendo o identificador
    (`schemas/pt-dglab.schema.json`) e recalcula apenas manifest.json.

    Mesma classe de ataque que R16, aplicada à segunda dependência que
    ADR-026 vincula por hash: um verificador que resolvesse o schema a
    partir do pacote (comportamento normativo, NDF-PKG-008) obteria um
    contrato diferente do que a entrada 'schema_perfil' de
    `dependencias_interpretacao` autentica.
    """
    relative = "schemas/pt-dglab.schema.json"
    path = root / relative
    schema = load(path)
    schema["properties"]["classificacao_ref"]["pattern"] = "^.*$"
    dump(path, schema)
    update_inventory_hash(root, relative)


def _schema_canonico_trocado(root: Path) -> None:
    """Troca o schema do tipo **canónico** (`oficio`, não extensão
    qualificada) mantendo o identificador, e recalcula apenas manifest.json.

    Reproduz revisão adversarial ao commit 3985001: a condição inicial de
    `schema_tipo` (só extensão qualificada) deixava um schema canónico
    transportado no pacote livre para ser substituído sem deteção —
    `schemas/oficio.schema.json` alterado passava. Corrigido tornando
    `schema_tipo` sempre obrigatório (§2.6.2, ADR-026, segunda ronda).
    """
    relative = "schemas/oficio.schema.json"
    path = root / relative
    schema = load(path)
    schema["description"] = schema.get("description", "") + " [ALTERADO]"
    dump(path, schema)
    update_inventory_hash(root, relative)


def _recurso_trocado(root: Path) -> None:
    """Troca um recurso do NDT (`recursos/`) referenciado por hash,
    mantendo o nome do ficheiro, e recalcula apenas manifest.json.

    Reproduz R23 (achado da revisão externa de 2026-09-11): antes desta
    verificação, `recursos[].hash_sha256` dentro do NDT não era confrontado
    com os bytes físicos — trocar o ficheiro passava.
    """
    candidatos = list((root / "recursos").glob("*.svg"))
    if not candidatos:
        raise RuntimeError("nenhum recurso .svg encontrado no pacote de exemplo")
    path = candidatos[0]
    path.write_bytes(b"<svg>recurso trocado, mesmo nome de ficheiro</svg>")
    update_inventory_hash(root, str(path.relative_to(root)))


def _recurso_candidatos_ambiguos(root: Path) -> None:
    """Dois ficheiros candidatos ao mesmo recurso: uma cópia legítima com
    outra extensão, e o ficheiro original (nome = hash correto) adulterado.

    Reproduz revisão adversarial ao commit f25a3bc: a resolução por
    `recursos/<hash>.*` verificava só `candidatos[0]` (ordem alfabética) e
    ignorava os restantes — uma cópia `.aaa` legítima ao lado do `.svg`
    adulterado passava, porque `.aaa` < `.svg`. Um renderizador que escolha
    por extensão ou tipo pode consumir precisamente o ficheiro nunca
    escrutinado. Corrigido: mais de um candidato é erro (NDF-PKG-011).
    """
    hash_hex = "32c937bf849181d3799a656e088b304f575311b141e557aba7682e50b38c3316"
    recdir = root / "recursos"
    legit = recdir / f"{hash_hex}.svg"
    copia = recdir / f"{hash_hex}.aaa"
    copia.write_bytes(legit.read_bytes())
    legit.write_bytes(b"<svg>adulterado</svg>")
    manifest_path = root / "manifest.json"
    manifest = load(manifest_path)
    for item in manifest["inventario"]:
        if item["ficheiro"] == f"recursos/{hash_hex}.svg":
            item["hash_sha256"] = "sha256:" + hashlib.sha256(legit.read_bytes()).hexdigest()
    manifest["inventario"].append({
        "ficheiro": f"recursos/{hash_hex}.aaa",
        "hash_sha256": "sha256:" + hashlib.sha256(copia.read_bytes()).hexdigest(),
    })
    dump(manifest_path, manifest)


def _dependencia_omitida(root: Path) -> None:
    """Remove do NDF-core a entrada 'schema_perfil' de
    `dependencias_interpretacao`, mantendo `avaliacao.perfil` declarado.

    NDF-PROD-025: quando `avaliacao.perfil` está declarado, tem de existir
    entrada correspondente. Omiti-la é tão inválido como declará-la errada —
    ambas deixam uma dependência de interpretação sem vínculo criptográfico.
    """
    core_path = root / "ndf-core.json"
    core = load(core_path)
    deps = core["dependencias_interpretacao"]
    core["dependencias_interpretacao"] = [d for d in deps if d.get("papel") != "schema_perfil"]
    dump(core_path, core)
    update_inventory_hash(root, "ndf-core.json")


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
