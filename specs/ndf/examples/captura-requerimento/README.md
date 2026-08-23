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

**Submeter não é produzir, e o exemplo separa as duas coisas.** O sistema
observou uma submissão autenticada no e-balcão; não observou quem escreveu o
PDF. Declarar o submissor como `autor` seria afirmar um facto que a captura não
estabelece — e §2.2.1 proíbe expressamente satisfazer o invariante de origem com
informação inventada. O pacote declara, por isso, três coisas distintas:

| O que se sabe | Onde se declara |
|---|---|
| Quem submeteu, por que canal, com que autenticação e a que horas | `documento.proveniencia_submissao` |
| Que a autoria material não é apurável, e porquê | `metadados.origem_nao_identificavel` (§2.2.1, ADR-023) |
| Quem responde juridicamente pelo documento, e a que título | `imputacao`, com o facto de autenticação que o produtor invoca (§2.15.4) |

Um sistema que disponha de prova independente da autoria material declara-a em
`participantes` e omite `origem_nao_identificavel` — os dois são mutuamente
exclusivos. O que não é admissível é derivar um do outro.

**`tipo_equivalente` está ausente.** O campo é opcional e declara-se «quando
determinável»: não há tipo nativo registado que corresponda a um requerimento de
cidadão, e preencher o campo com o tipo mais próximo produziria uma medida de
transição falsa (registo, §3.2.4).

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
