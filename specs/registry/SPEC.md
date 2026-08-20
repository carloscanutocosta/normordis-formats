# Registo NORMORDIS — Tipos de documento

**Versão**: 1.0.0  
**Estado**: Draft — revisão pública por abrir

---

## 1. Propósito

O registo define o mecanismo de resolução de `tipo_documento_ref` — o campo do NDF-core que identifica o schema da estrutura interna de `documento`. Cada entrada do registo é um schema JSON (JSON Schema Draft 2020-12) que valida o conteúdo de `documento` para um tipo específico.

---

## 2. Formato do identificador

```
<id>@<versao>
```

| Componente | Regras | Exemplos |
|---|---|---|
| `id` | Lowercase, hífens, sem espaços; estável (não muda com versões) | `oficio`, `informacao-tecnica`, `despacho`, `parecer`, `modelo3-irs` |
| `versao` | SemVer 2.0.0 para tipos normativos; `YYYY.N` para impressos com versão anual | `1.0.0`, `2026.1` |

---

## 3. Tipos canónicos (esta especificação)

| `tipo_documento_ref` | Descrição | Schema |
|---|---|---|
| `oficio@1.0.0` | Ofício — comunicação formal externa | [schemas/oficio.schema.json](schemas/oficio.schema.json) |
| `informacao-tecnica@1.0.0` | Informação técnica — nota interna fundamentada | [schemas/informacao-tecnica.schema.json](schemas/informacao-tecnica.schema.json) |
| `parecer@1.0.0` | Parecer — apreciação fundamentada com sentido explícito, sobre outro documento | [schemas/parecer.schema.json](schemas/parecer.schema.json) |
| `despacho@1.0.0` | Despacho — decisão ou instrução de serviço | [schemas/despacho.schema.json](schemas/despacho.schema.json) |
| `documento-capturado@1.0.0` | Documento cujo conteúdo reside em componentes binários — emitido fora do editor estruturado ou recebido do exterior | [schemas/documento-capturado.schema.json](schemas/documento-capturado.schema.json) |

`informacao-tecnica`, `parecer` e `despacho` formam, em conjunto com
`NDF-core.relacoes` (SPEC.md §2.11), a cadeia documental
Informação → Parecer → Despacho — três documentos NDF autónomos ligados por
relações verificáveis, nunca um único documento com secções sucessivamente
assinadas. Ver exemplo em `specs/ndf/examples/informacao-parecer-despacho/`.

`documento-capturado` distingue-se dos restantes por não conter o corpo do ato:
transporta a casca descritiva e os componentes binários que o constituem. É um
NDF completo em tudo o resto — identidade, proveniência, imputação, avaliação,
relações, integridade e custódia. Ver
[ADR-020](../../docs/architecture/ADR-020-um-formato-duas-realidades.md).

É **um** tipo genérico, e não uma família (`oficio-capturado`,
`parecer-capturado`, …): o campo opcional `tipo_equivalente` transporta a
correspondência com o tipo nativo sem duplicar o registo.

Tipos específicos de cada entidade (AT, SS, Municípios, etc.) são definidos fora desta especificação base mas seguem o mesmo formato de schema.

---

## 3.1 Perfis de avaliação arquivística

Além dos tipos documentais, o registo mantém os **perfis de avaliação
arquivística** referenciados por `NDF-core.avaliacao.perfil` (SPEC.md §3.2.3).
Um perfil restringe o bloco `avaliacao` ao vocabulário e à sintaxe de uma
jurisdição, sem alterar a estrutura fixada pelo NDF-core.

| `avaliacao.perfil` | Âmbito | Schema |
|---|---|---|
| `pt-dglab` | Administração Pública portuguesa — MEG/DGLAB | [profiles/pt-dglab.schema.json](profiles/pt-dglab.schema.json) |
| `generic` | Sem restrições jurisdicionais | [profiles/generic.schema.json](profiles/generic.schema.json) |

O schema do perfil declarado **DEVE viajar dentro do `.ndfpkg`**, em
`schemas/<perfil>.schema.json` (NDF-PKG-008). Perfis de outras jurisdições são
acrescentados a este registo sem alteração incompatível do NDF-core, mediante
confirmação contra os instrumentos legais da jurisdição respetiva.

O identificador de perfil é opaco e qualificado — dois ou mais segmentos, o
primeiro tipicamente o código da jurisdição, o segundo a **autoridade** com
competência sobre o regime e não o instrumento que ela publica. Perfis já
mapeados mas ainda sem schema publicado (`fr-siaf`, `de-barch`, `nl-na`,
`eu-ec`) estão documentados em
[`docs/profiles/`](../../docs/profiles/README.md).

---

## 3.2 Via de produção admissível por tipo

Um documento pode nascer por duas vias: **estruturada** — editor que produz
`documento` tipado, com NDT e NCRTF — ou **capturada** — binário emitido fora do
sistema estruturado e preservado como componente
(`documento-capturado@<versao>`). As duas produzem NDF completos e distinguem-se
apenas no bloco `documento` e na função do NDT; ver
[`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../../docs/design/NDFPKG-CAPTURA-E-INGESTAO.md) §3.

Enquanto o editor estruturado não cobrir uma tipologia, a via capturada é o
regime corrente dessa tipologia. À medida que passa a cobri-la, a tipologia
transita. O registo dá o **lugar onde essa transição se declara**; não a decide.

### 3.2.1 Declaração

Cada entrada do registo PODE declarar:

| Campo | Valores | Significado |
|---|---|---|
| `via_predefinida` | `estruturada` \| `capturada` | A via que o sistema propõe por omissão para este tipo |
| `captura_admissivel` | `true` \| `false` | Se o tipo aceita `documento-capturado` como forma válida de o produzir |

Na ausência de declaração, o tipo não impõe restrição — a decisão é inteiramente
da entidade que o usa.

### 3.2.2 Quem declara o quê

O registo canónico define o **mecanismo** e PODE registar um valor recomendado.
O valor em vigor num organismo é declarado por esse organismo. Isto decorre do
princípio de que ao formato compete permitir que a informação relevante seja
guardada, não impor a decisão de quem produz (SPEC NDF §1.1; ver
[`ROADMAP.md`](../../ROADMAP.md), decisão de âmbito de 2026-08-20).

Um organismo PODE apertar o valor recomendado — passar `captura_admissivel` de
`true` a `false`. NÃO DEVERIA alargá-lo sem justificação registada.

### 3.2.3 Roquete, não interruptor

A transição é **unidirecional por desenho**. `captura_admissivel` move-se de
`true` para `false` quando o editor passa a cobrir o tipo; voltar atrás exige
justificação expressa e registada, com data e responsável.

Sem esta regra, a declaração seria um interruptor e o regime de transição
converter-se-ia em permanente por inércia — que é o risco principal desta
matéria, não a decisão inicial.

### 3.2.4 Valores recomendados para os tipos canónicos

| Tipo | `via_predefinida` | `captura_admissivel` | Nota |
|---|---|---|---|
| `oficio@1.0.0` | `estruturada` | `true` | Enquanto o editor não cobrir a tipologia |
| `informacao-tecnica@1.0.0` | `estruturada` | `true` | idem |
| `parecer@1.0.0` | `estruturada` | `true` | idem |
| `despacho@1.0.0` | `estruturada` | `true` | idem |
| `documento-capturado@1.0.0` | `capturada` | — | O campo não se aplica: o tipo **é** a via |

`captura_admissivel: true` é aqui reconhecimento do estado presente, não
recomendação permanente. Pelo roquete de §3.2.3, cada um destes valores passa a
`false` quando o editor cobrir a tipologia, e não volta atrás sem justificação
registada.

### 3.2.5 Alteração

Alterar qualquer dos dois campos é alteração do registo, com data e
responsável. Não é alteração do NDF-core nem de `tipo_documento_ref`: nenhum
documento já produzido é afetado, porque a declaração governa a **produção
futura**, nunca a validade do que existe.

### 3.2.6 Medida de progresso da transição

A proporção de documentos produzidos por via estruturada face aos capturados,
**por tipo**, é o indicador que informa duas decisões: onde investir a seguir no
editor, e quando acionar o roquete de §3.2.3.

Contrato do indicador:

| | |
|---|---|
| **Universo** | documentos finalizados de uma entidade, num intervalo declarado |
| **Numerador** | documentos cujo `metadados.tipo_documento_ref` **não** seja `documento-capturado@<versao>` |
| **Denominador** | os anteriores, mais os capturados |
| **Agrupamento** | por tipo. Nos capturados, o tipo de agrupamento é `documento.tipo_equivalente` quando declarado; sem ele, o documento conta para um agregado «sem tipo equivalente» |
| **Fonte** | `metadados.tipo_documento_ref` e `documento.tipo_equivalente` — nenhum campo novo é necessário |

É informação **derivada e operacional**, fora do NDF (SPEC §3.6): recalculável a
partir do corpus, nunca armazenada nele. O registo fixa aqui o que se conta e a
partir de quê; quem o calcula é o sistema que detém o corpus.

O agregado «sem tipo equivalente» é deliberado. Um capturado que não consiga
nomear o tipo nativo correspondente é sinal de que a tipologia não está
modelada, o que é informação de roadmap tão útil quanto a proporção em si.

---

## 4. Resolução

Um leitor NDF resolve `tipo_documento_ref` na seguinte ordem de precedência:

1. **`.ndfpkg`**: se presente no pacote de exportação, o schema fica em `registry/<tipo_documento_ref>.schema.json` dentro do ZIP.
2. **Registo local**: implementação mantém uma cópia local dos schemas canónicos.
3. **Registo remoto** (roadmap): URI canónico `https://registry.normordis.pt/<id>/<versao>/schema.json`.

---

## 5. Compatibilidade

Segue as mesmas regras SemVer da especificação NDF (§7):
- `MINOR`: adição de campos opcionais; leitores antigos podem preservar o
  objeto como opaco ou recusá-lo, mas não ignoram silenciosamente conteúdo
  assinado desconhecido.
- `MAJOR`: mudança incompatível — leitores recusam processar.

Um leitor só declara interpretação completa das versões que suporta
explicitamente.
