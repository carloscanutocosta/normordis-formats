# NDT Roadmap

## v2.0.0 — Em implementação

Spec estável. Ver [SPEC.md](SPEC.md) e [CHANGELOG.md](CHANGELOG.md).

Âmbito implementado:
- Layout prescritivo para PDF/UA-2 (graficos[], campos[], blocos[], fluxo, sequencia[])
- Modelo de fluxo para documentos administrativos (fluxo + linha_lateral + quebra_pagina)
- Assinatura híbrida CAdES-B-LTA + PAdES (modo: "hibrido")
- Estilos globais para renderizadores ODF/HTML (estilos)
- Dados NDF em cabeçalhos de página (campo_ndf, {ndf:caminho} em mobilia[])
- Acessibilidade PDF/UA-2 + arquivo PDF/A-3 (alt, rotulo_acessivel)
- Composição de documentos (composicao[])
- ODF como formato secundário (intercâmbio e edição)

---

## v2.1 — Planeado

### T1. Rodapé de tabela (`rodape` em `blocos[].tabela`)

**Problema**: em tabelas com posicionamento absoluto (`blocos[]`), não há forma de declarar uma linha de rodapé (totais, subtotais) que siga o fim dos dados NDF. Em contexto `fluxo` existe um contorno adequado (`campo` após `tabela` em `fluxo.elementos`); em `blocos[]` absolutos, o total tem de ser posicionado em coordenadas fixas — o que falha quando a tabela transborda para páginas seguintes.

**Solução proposta**:

```json
{
  "tipo": "tabela",
  "referencia": "quadro4.imoveis",
  "posicao": { "x": 15, "y": 50 },
  "largura": 180,
  "min_linhas_visivel": 8,
  "colunas": [...],
  "rodape": {
    "linhas": [
      {
        "celulas": [
          { "coluna_id": "descricao", "conteudo_fixo": "Total" },
          { "coluna_id": "valor_realizacao", "referencia": "quadro4.total_realizacao", "formato": "monetario" },
          { "coluna_id": "mais_valia", "referencia": "quadro4.total_mais_valias", "formato": "monetario" }
        ],
        "estilo": { "fundo": "#EEEEEE", "fonte": { "peso": "bold" } }
      }
    ]
  }
}
```

O rodapé renderiza sempre após a última linha de dados, em todas as páginas onde a tabela termina. Em páginas intermédias de overflow, o rodapé não aparece.

**Casos de uso**: relatórios financeiros, quadros de apuramento fiscal, mapas de pessoal.

---

### T2. Agrupamento de linhas em tabela (`cabecalho_grupo`)

**Problema**: tabelas com sub-cabeçalhos de categoria (ex.: "Prédios Urbanos" → linhas → "Prédios Rústicos" → linhas) não são expressáveis numa única `tabela`. O contorno actual — tabelas separadas com `texto_fixo` entre elas em `fluxo` — é funcional mas verboso e não permite `min_linhas_visivel` por grupo.

**Solução proposta**: o NDF pode marcar itens do array como cabeçalhos de grupo através de um campo discriminante; o NDT declara como renderizá-los:

```json
{
  "tipo": "tabela",
  "referencia": "mapa.linhas",
  "agrupamento": {
    "campo_discriminante": "tipo_linha",
    "valor_cabecalho": "cabecalho_grupo",
    "estilo_cabecalho": {
      "fundo": "#DDDDDD",
      "fonte": { "peso": "bold" },
      "colspan_total": true
    }
  },
  "colunas": [...]
}
```

O NDF estrutura o array com itens marcados como `"tipo_linha": "cabecalho_grupo"` (e.g. `{ "tipo_linha": "cabecalho_grupo", "descricao": "Prédios Urbanos" }`) intercalados com linhas de dados normais. O renderizador detecta os itens marcados e renderiza-os como linhas de cabeçalho de grupo.

**Nota de design**: o campo `campo_discriminante` não é lógica de negócio no NDT — é uma instrução de renderização sobre como interpretar estrutura já presente no NDF. A decisão de quais itens são cabeçalhos é da aplicação de domínio.

**Casos de uso**: mapas de pessoal por categoria, balanços por natureza de rubrica, relatórios financeiros com grupos de contas.

---

### T3. Verificação de cobertura NCRTF v2.0.0

**Problema**: o `corpo` do NDT referencia conteúdo NCRTF do NDF. A qualidade do saída ODF/HTML para documentos administrativos depende diretamente do que o NCRTF expressa. Padrões a verificar antes de implementar o renderizador ODF:

**Verificação concluída** contra NCRTF v2.0.0 (§4, §5, §6, §11.3):

| Padrão | Status NCRTF v2.0.0 | Impacto se ausente |
|---|---|---|
| Notas de rodapé | **Ausente** | Documentos legais e contratos |
| Referências cruzadas internas | **Ausente** | Despachos com remissão para artigos |
| Listas numeradas multi-nível | Parcial — `list`/`list_item` existem; `start` é candidato futuro (§11.3) e não há estilo de numeração por nível | Normas, regulamentos, articulado legal |
| Tabelas com colspan/rowspan em corpo | **Ausente** | Relatórios técnicos |
| Citações em bloco | **Coberto** — `blockquote` (§4.4) | Pareceres jurídicos |

Lacuna adicional identificada na mesma verificação: as células de `table` são strings de texto plano (§4.5), sem formatação inline. Já consta de §11.3 do NCRTF como candidato ("Rich text em células de tabela").

Todos os padrões em falta são **aditivos** na política de extensão do NCRTF (§11.1: novo nó bloco opcional ou novo campo opcional ⇒ MINOR). A solução é na spec NCRTF — o NDT não precisa de ser alterado.

**Critério de importação a partir do ODF**: o ODF é a referência de vocabulário para o que falta, mas nem tudo o que o ODF exprime pertence ao NCRTF. Importa-se o que é *estrutura semântica de texto finalizado* — notas, remissões, numeração por nível, células ricas. Não se importa o que é *estado de edição*: `text:tracked-changes` e `office:annotation` colidem com a imutabilidade do NDF. Nem o que é *apresentação*, que pertence ao NDT.

O estudo completo — incluindo as lacunas do próprio NDT face ao ODF, as decisões de fronteira NDT↔NCRTF e o plano faseado — está em [`docs/design/ODF-ALIGNMENT-STUDY.md`](../../docs/design/ODF-ALIGNMENT-STUDY.md).

---

### T4. `corpo`/`texto` de `informacao-tecnica`, `parecer` e `despacho` não é NCRTF — IMPLEMENTADO (2026-09-06)

**Problema**, identificado ao construir os primeiros exemplos destes três tipos
(`specs/ndt/examples/informacao-tecnica.ndt.json`, `parecer.ndt.json`,
`despacho.ndt.json`): a SPEC (§9.1) lista precisamente estes três tipos —
a par de ofício e diploma legal — como exemplos do perfil **"Texto corrido"**,
cujos requisitos críticos incluem `NDT-PROD-008`/`009` (exclusividade
`fluxo`/`blocos[]`, corpo único por fluxo) e `NDT-RENDER-009` (extravasamento
do `corpo`). Mas `informacao-tecnica.corpo`, `informacao-tecnica.conclusao`,
`informacao-tecnica.proposta_despacho`, `parecer.corpo`/`conclusao`/`condicoes`
e `despacho.texto` são todos **strings simples** nos schemas do registo
(`specs/registry/schemas/`) — não valores NCRTF. O schema do `parecer` já
regista isto como "dívida técnica pré-existente".

**Consequência prática**: o elemento `tipo: "corpo"` (§5.2.1, §5.5.2) exige
explicitamente um valor NCRTF — não pode ser usado para estes três tipos. Os
exemplos criados recorrem a `tipo: "campo"` (§5.4) como única alternativa
viável, o que expõe duas lacunas que só aparecem com um valor de texto longo:

1. `campo` em `fluxo.elementos` não tem, ao contrário de `texto_fixo`
   (§5.2.1: *"faz wrapping automático na largura disponível"*), nenhuma
   garantia documentada de *word-wrap* multi-linha para um valor NDF longo.
2. `sequencia[].repeticao: "conforme_necessario"` (§5.7) só define
   extravasamento para um array (`itens`) ou para "conteúdo NCRTF por
   colocar" — nunca para uma string escalar. Um `despacho.texto` ou
   `parecer.corpo` que não caiba numa página cai em comportamento não
   definido pela SPEC.

**Solução implementada** — com um ajuste de âmbito face à proposta inicial:
migrados apenas os três campos de **corpo principal** —
`informacao-tecnica.corpo`, `parecer.corpo`, `despacho.texto` — para o mesmo
objeto NCRTF já usado por `oficio.corpo`. `informacao-tecnica.conclusao`/
`.proposta_despacho` e `parecer.conclusao`/`.condicoes` **mantiveram-se
string**: são sínteses curtas por desenho, sem caso de uso para rich text, e
migrá-los colidiria com `NDT-PROD-009` (um único elemento `corpo` por
`fluxo`) — um `fluxo` com dois ou três campos NCRTF independentes não tem hoje
forma de os intercalar. Resolve as duas lacunas de wrapping/extravasamento
para o campo que de facto precisa delas, sem reabrir essa outra questão sem
necessidade real.

Alteração **incompatível** nos três schemas do registo (campo obrigatório
muda de tipo) — sobem para v2.0.0 (`informacao-tecnica@2.0.0`,
`parecer@2.0.0`, `despacho@2.0.0`), SemVer MAJOR por `VERSIONING.md`.
`ndt_version_ref` (identidade do template NDT) é independente e não é
afetado. O exemplo assinado
`specs/ndf/examples/informacao-parecer-despacho/` foi recanonicalizado com os
novos `payload_hash`; no processo foi encontrada e corrigida uma divergência
pré-existente entre `sobre[]` e `relacoes[]` nesse mesmo exemplo, e fechada a
lacuna do verificador que deveria tê-la apanhado (L5, ver
`specs/ndf/CHANGELOG.md`).

**Esforço**: **P** por schema — realizado. Ver `specs/ndt/CHANGELOG.md` e
`specs/ndf/CHANGELOG.md` (2026-09-06).

---

### T5. Rotação de valores NDF em `campos[]` (texto vertical em impressos) — IMPLEMENTADO (2026-09-06)

**Problema**: `rotacao` está definido em **todos** os elementos de
`graficos[]` (`linha`, `rectangulo`, `imagem`, `texto_fixo`, `grelha_digitos`,
`codigo_barras`, `poligono`, `elipse`, `svg`, `tabela_visual` — confirmado
contra `specs/ndt/schemas/ndt.schema.json`), mas **não** em `Campo` (§5.4),
nem em `ColunaTabela`, nem em `MobiliaCampoNdf` (§5.6). Um valor estático pode
ser impresso a qualquer ângulo; um valor **vindo do NDF** só pode hoje, se
precisar de rotação, se for dígito-a-dígito (`grelha_digitos`) ou codificado
(`codigo_barras`) — ambos em `graficos[]`. Um campo de texto simples com um
valor de dados (referência de arquivo na margem lateral de um impresso,
carimbo de registo lido de baixo para cima, código de lote na lombada de um
formulário) não tem forma de ser rodado.

**Casos de uso**: margens de arquivo lateral em processos físicos
digitalizados, carimbos de registo cadastral, formulários com campos na
lombada ou no verso.

**Solução implementada**: `rotacao` (opcional, `number`, default `0`)
acrescentado a `Campo` (§5.4) e a `MobiliaCampoNdf` (§5.6) — alteração
aditiva, sem impacto em templates existentes. `ColunaTabela` fica de fora
deliberadamente: rodar uma célula exigiria rodar a própria estrutura da
tabela, problema de layout distinto e sem caso de uso documentado.

**Esforço**: **P**. Ver CHANGELOG (2026-09-06).

---

### T6. Arrays de valores escalares sem primitiva de renderização — IMPLEMENTADO (2026-09-06)

**Problema**, também identificado ao construir o exemplo de `parecer`:
`parecer.fundamentacao_juridica` é um array de **strings simples** (ex.:
`"CPA, Art.º 61.º"`), não de objetos. `blocos[].tabela` e a `tabela` de
`fluxo.elementos` (§5.5.1, §5.2.1) só sabem iterar um array de **objetos**,
porque `colunas[].id` referencia sempre "propriedade do item NDF" — um item
escalar não tem propriedade nenhuma a referenciar. Não há, hoje, primitiva
NDT para apresentar um array de valores simples como lista (bullet ou
numerada) ligada a dados. O exemplo `parecer.ndt.json` deixa
`fundamentacao_juridica` por renderizar por esta razão — é o próprio limite
do formato, não uma omissão do exemplo.

**Solução implementada** (SPEC §5.5.4): um novo elemento `lista`, na mesma dupla colocação de
`tabela` — `blocos[]` (absoluto, com `posicao`) e `fluxo.elementos` (sem
`posicao`) — para um array NDF de escalares, tal como `tabela` já serve o
array de objetos.

```json
{
  "tipo": "lista",
  "referencia": "fundamentacao_juridica",
  "formato": "texto",
  "estilo": "bullet",
  "marcador": "—",
  "espacamento_entre_itens_mm": 1.5
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `referencia` | Sim | Caminho NDF do array de escalares. |
| `posicao`, `largura` | Cond. | Como em `tabela` — obrigatórios em `blocos[]`, omitidos em `fluxo.elementos`. |
| `formato` | Não | Formato de apresentação por item (§4.3). Predefinição `"texto"`. |
| `estilo` | Não | `"bullet"` \| `"numerado"`. Predefinição `"bullet"`. |
| `marcador` | Não | Carácter do marcador quando `estilo: "bullet"`. Predefinição `"•"`. Sem efeito em `"numerado"`. |
| `espacamento_entre_itens_mm` | Não | Espaço vertical entre itens. |

Decisões de desenho, por esta ordem de importância:

1. **Sem `colunas[]`** — a diferença estrutural que justifica um elemento
   novo em vez de estender `tabela`: um item escalar não tem propriedades
   a mapear.
2. **Um só nível.** Ao contrário de `list`/`list_item` do NCRTF (conteúdo
   editado à mão, aninhamento genuíno), aqui o array vem do NDF —
   `fundamentacao_juridica` é sempre plano. Aninhamento fica por fazer até
   haver um array de arrays real (teste de admissão, ADR-015).
3. **`estilo: "numerado"` sem parâmetro de formato próprio** — reutiliza,
   quando existir, `estilos.listas[]` da Fase A do NCRTF (T3/A3 acima) em
   vez de inventar um segundo vocabulário de numeração no mesmo documento.
   Até A3 estar implementado, `"numerado"` usa `1.`, `2.`, `3.` fixo.
4. **Overflow como `tabela`**: participa em `sequencia[]` do mesmo modo —
   `repeticao: "conforme_necessario"` com `fonte_overflow` a apontar para o
   array. Não é caso novo, é o mecanismo que já existe para arrays.

**Depende de**: nada bloqueante — `estilo: "numerado"` usa por agora `1.`,
`2.`, `3.` fixo; o comportamento fino melhora quando A3 (Fase A do NCRTF)
chegar, sem alteração ao schema desta cláusula.

`parecer.ndt.json` usa `lista` para `fundamentacao_juridica` (fluxo, entre o
corpo e a conclusão). Vetor de conformidade em
`conformance/ndt/valid/bloco-lista.json`, cobrindo `blocos[]` absoluto e
`fluxo.elementos`.

**Esforço**: **M** — realizado.

---

## Fora de âmbito (por design)

Os seguintes padrões foram analisados e excluídos deliberadamente:

| Padrão | Razão da exclusão |
|---|---|
| Colspan/rowspan em `blocos[].tabela` | `tabela_visual` (graficos[]) cobre a estrutura; `blocos[].tabela` cobre os dados — a combinação é suficiente para impressos fiscais |
| Texto em múltiplas colunas (newspaper) | Raro em AP; sem pedido documentado |
| Herança de template (NDT estende NDT) | Preocupação de ferramentas, não de formato; resolve-se ao nível do editor/SDK |
| Hiperligações em `campos[]` | NCRTF no `corpo` cobre links; campos posicionados raramente são hiperligáveis em documentos oficiais |
| Estilos condicionais por valor (ex.: vermelho se negativo) | Lógica de apresentação baseada em dados = lógica de negócio; responsabilidade da aplicação de domínio |
| Numeração automática de linhas de tabela | A aplicação de domínio inclui o número no NDF; o renderizador não computa valores |
| Camada de formulário unificada (dados + layout + cálculo + scripts) ao estilo XFA (Adobe) | Historicamente resolveu o mesmo problema dos impressos legais (§9.1, perfil "Impresso"), mas era proprietária, mal suportada fora do Acrobat/LiveCycle, e **removida do próprio PDF na norma ISO 32000-2 (PDF 2.0)**. O acoplamento dados+layout+cálculo num único ficheiro é exatamente o que o NDT evita ao separar NDT (layout) de NDF (dados) e deixar cálculo à aplicação de domínio (§1, ponto 1). Registado aqui como precedente de cautela, não como candidato |
