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

| Padrão | Status NCRTF v2.0.0 | Impacto se ausente |
|---|---|---|
| Notas de rodapé | A verificar | Documentos legais e contratos |
| Referências cruzadas internas | A verificar | Despachos com remissão para artigos |
| Listas numeradas multi-nível | A verificar (list_item existe) | Normas, regulamentos |
| Tabelas com colspan/rowspan em corpo | A verificar | Relatórios técnicos |
| Citações em bloco | A verificar | Pareceres jurídicos |

Se algum padrão estiver ausente do NCRTF, a solução é na spec NCRTF — o NDT não precisa de ser alterado.

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
