# Exemplo `.ndfpkg` — documento capturado

Este diretório representa o conteúdo interno de um `.ndfpkg` de um **documento
capturado**: um requerimento submetido por um cidadão via e-balcão, cujo
conteúdo reside num componente binário e não em `documento` (SPEC §2.8.1,
[ADR-020](../../../../docs/architecture/ADR-020-um-formato-duas-realidades.md)).

```bash
zip -r ../captura.ndfpkg manifest.json ndf-core.json envelope.json \
       ndt/ schemas/ original/
```

## Ficheiros

| Ficheiro | Descrição |
|---|---|
| `manifest.json` | Inventário físico com hashes |
| `ndf-core.json` | Bytes canónicos JCS/RFC 8785 |
| `envelope.json` | `payload_hash`, `validation_code`; sem assinaturas (`nivel_assinatura: "nenhuma"`) |
| `ndt/documento-capturado@1.0.0.ndt.json` | NDT do **auto de captura** — descreve a captura, não o documento |
| `schemas/` | Schemas necessários à validação autónoma, incluindo o do tipo capturado e o perfil `pt-dglab` |
| `original/requerimento.pdf` | O componente. 627 bytes, gerado de forma determinística |

## O que este exemplo demonstra

**O componente está preso aos bytes assinados.** `documento.componentes[0].sha256`
entra nos `payload_bytes`; `manifest.inventario` transporta o mesmo digest. A
junta entre os dois é `NDF-PKG-009`, e fecha nos dois sentidos.

**Deficiência registada, não emendada.** O PDF não é conforme a PDF/A e diz-se:
`validacao_formato.resultado: "nao_conforme"`, com validador, versão e instante.
`reconstituicao.estado` é `adequada_com_deficiencia`, com fundamento. Ao
contribuinte não se exigem formalidades de formato além da autenticação no
portal — a deficiência é propriedade do que chegou, nunca fundamento de recusa
da submissão.

**O invariante de origem aplica-se.** `participantes` declara o submissor como
`autor`: a captura não dispensa declarar quem produziu o documento, apenas
desloca o objeto dessa produção do texto para o componente (§2.2.1, §2.8.1).

**`nivel_assinatura` é `"nenhuma"`.** É o nível de assinatura **do NDF**. Um
requerimento sem assinatura eletrónica própria não deixa de ser custodiável, e
o nível nunca se herda de assinaturas contidas em componentes (§4.5.1).

## Reprodutibilidade

O componente é gerado por
[`tools/scaffold_captura_fixture.py`](../../../../tools/scaffold_captura_fixture.py),
sem dependências externas e com bytes idênticos em qualquer máquina:

```bash
python3 tools/scaffold_captura_fixture.py
# requerimento.pdf: 627 bytes, sha256:9741495bbc5aa8f2575339e28eb60663d1c480cfa3d4df41f20cb486cd88a053
```

O PDF é deliberadamente simples — sem fontes embebidas, sem metadados XMP —
para que o exemplo exercite o caso de não conformidade em vez do caso feliz.

## Vetores negativos derivados deste pacote

`PKG-NEG-010` a `PKG-NEG-014` em
[`tools/check_package_vectors.py`](../../../../tools/check_package_vectors.py):
componente ausente do pacote; digest divergente entre declaração e inventário;
ficheiro em `original/` não declarado; original reescrito com o NDF-core
harmonizado; documento capturado sem estado de reconstituição.

`PKG-NEG-011` é o que motivou [ADR-021](../../../../docs/architecture/ADR-021-componentes-nos-bytes-assinados.md):
sem `NDF-PKG-009`, alterar o componente e regerar o manifesto produziria um
pacote que passa em toda a validação, porque a assinatura cobre o NDF-core e o
manifesto não é assinado.
