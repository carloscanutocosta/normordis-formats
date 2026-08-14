# Generalização do bloco `avaliacao` e separação custódia ↔ RGPD

**Estado:** proposta de desenho, aceite para execução em 1.0.0
**Data:** 2026-08-14
**Origem:** revisão externa (2026-08-14) que reidentificou o risco R11; decisão
do responsável do projeto de o resolver antes da abertura de revisão pública,
por o objetivo mais próximo ser uma candidatura NGI/OSOR.

Este documento fixa o desenho. As decisões estão registadas em
[ADR-015](../architecture/ADR-015-generalizacao-avaliacao-arquivistica.md) e
[ADR-016](../architecture/ADR-016-custodia-vs-responsavel-tratamento.md).

---

## 1. Problema

### 1.1 `avaliacao` acoplada ao modelo arquivístico português

O bloco `avaliacao` do NDF-core é obrigatório e exige quatro campos cujo
vocabulário é o do MEG/DGLAB: `tipo_classificacao_ref`,
`prazo_conservacao_administrativa` (PCA), `destino_final` (DF) e
`instrumento_avaliacao_versao_ref`. O enum de `destino_final` tem exatamente os
três valores do modelo português.

Consequência: uma entidade fora de Portugal só produz um NDF válido se declarar
valores num vocabulário que não é o seu. O risco está registado como **R11** em
[`READINESS-ASSESSMENT.md`](../reports/READINESS-ASSESSMENT.md) e como item de
v2.0.0 em [`ROADMAP.md`](../../ROADMAP.md), em ambos os casos sem ação prevista.

### 1.2 `responsavel_tratamento` confunde dois conceitos

`metadados.responsavel_tratamento` é o responsável pelo tratamento na aceção do
RGPD (Art.º 13.º–14.º), mas o schema exige-o **sempre**, incluindo quando
`contem_dados_pessoais: false`. A SPEC justifica-o com um conceito diferente —
"identifica o responsável pela custódia do registo". São coisas distintas:
custódia institucional de um registo e responsabilidade pelo tratamento de
dados pessoais não coincidem necessariamente, e a segunda só existe quando há
dados pessoais.

Efeito prático: o formato força uma declaração RGPD sem facto RGPD subjacente, e
não permite detetar a incoerência inversa (declarar responsável pelo tratamento
num documento que afirma não conter dados pessoais).

---

## 2. Avaliação da premissa: o modelo PT é representativo?

A generalização só faz sentido se o modelo português for uma instância de um
padrão mais amplo. Levantamento feito em 2026-08-14 sobre cinco sistemas:

| Sistema | Prazo | Destino final | Instrumento |
|---|---|---|---|
| **PT** — MEG/DGLAB | PCA (valor + unidade + forma de contagem) | conservação permanente / eliminação / conservação parcial por amostragem | Lista Consolidada, Tabela de Seleção, Portaria |
| **FR** — SIAF | DUA (durée d'utilité administrative) | **C** conservation / **E** élimination / **T** tri | tableau de gestion |
| **NL** — Archiefwet / MDTO | bewaartermijn | blijvend te bewaren / te vernietigen / **voorlopig te bewaren** / **nader te bepalen** | selectielijst |
| **DE** — Bund/Länder | Aufbewahrungsfrist | **Anbietung**: a entidade oferece, o arquivo aprecia (Bewertung) → Übernahme ou Vernichtung | VwV Aufbewahrung und Aussonderung; Bundesarchivgesetz |
| **UK / CoE / Comissão Europeia** | retention period + trigger | destroy / **review** / transfer | retention & disposal schedule; Common Retention List |

**Conclusão.** O invariante `gatilho + prazo + ação de destino + instrumento que
a autoriza` está presente em todos. PT e FR são praticamente isomórficos,
incluindo o terceiro valor (amostragem / *tri*), que é a parte menos óbvia do
modelo. O modelo português **não é idiossincrático**: é uma instância nacional de
um padrão europeu comum.

Três divergências reais, todas aditivas:

1. **Decisão diferida não é exprimível.** NL tem dois valores para isto
   (`voorlopig te bewaren`, `nader te bepalen`); UK, Conselho da Europa e
   Comissão Europeia têm `review`. O enum fechado do NDF não os acomoda.
2. **Na Alemanha o destino não é decidido pelo produtor.** A entidade tem
   `Anbietungspflicht` — oferece ao arquivo, que aprecia a
   `Archivwürdigkeit`. No momento da finalização, o produtor **não pode**
   preencher `destino_final` com honestidade. Este é o único ponto que torna o
   formato inutilizável fora do padrão latino. Resolve-se com o mesmo valor do
   ponto 1.
3. **`conservacao_permanente` funde "conservar" com "transferir para o arquivo
   competente"** (FR distingue *versement*; DE *Übernahme*). Divergência menor;
   **não** é resolvida nesta ronda — ver §6.

### 2.1 Confiança das fontes

O levantamento assenta em fontes secundárias e de divulgação, não em textos
legais primários. É suficiente para decidir a arquitetura — o invariante é
estável nas cinco fontes — e **não é suficiente para publicar perfis
nacionais**. Por isso esta ronda cria apenas dois perfis (§3.3): `pt-dglab`,
fundamentado nos instrumentos que o projeto já usa, e `generic`, sem restrições
jurisdicionais. Perfis `fr-siaf`, `nl-na`, `de-bund` e `eu-crl` ficam como
candidatos documentados, a confirmar contra fonte primária antes de existirem.

---

## 3. Desenho — `avaliacao`

### 3.1 Forma

```json
{
  "avaliacao": {
    "perfil": "pt-dglab",
    "classificacao_ref": "lc/450.10.001",
    "instrumento_ref": "lc/lista-consolidada-dglab-2023-v3",
    "prazo_conservacao": {
      "valor": 5,
      "unidade": "anos",
      "forma_contagem": "data_documento"
    },
    "destino_final": "eliminacao"
  }
}
```

Campos obrigatórios: `perfil`, `classificacao_ref`, `instrumento_ref`,
`prazo_conservacao`, `destino_final`.

### 3.2 Alterações face a 1.0.0-draft anterior

| Antes | Depois | Motivo |
|---|---|---|
| — | `perfil` | Discriminador do sistema arquivístico aplicável. Novo, obrigatório. |
| `tipo_classificacao_ref` | `classificacao_ref` | `tipo_` era ruído; o campo é a referência da classe/série. |
| `instrumento_avaliacao_versao_ref` | `instrumento_ref` | Nome mais curto; a versão faz parte do valor, não do nome do campo. |
| `prazo_conservacao_administrativa` | `prazo_conservacao` | "administrativa" é o **A** de PCA — termo legal português. |
| `destino_final` (3 valores) | `destino_final` (4 valores) | Acrescenta `a_determinar`. |
| — | `autoridade_avaliacao` | Obrigatório se e só se `destino_final: "a_determinar"`. |

`destino_final` mantém o nome: traduz-se diretamente para *sort final* (FR),
*disposition* (UK/EN) e *Bewertungsentscheidung* (DE). `forma_contagem` mantém-se
sem alteração — os quatro valores atuais cobrem DE (`Ablauf des Kalenderjahres`
= `fim_ano_civil`) e FR sem acréscimos.

**Novo valor `a_determinar`**: a decisão de destino final não está tomada no
momento da finalização, por competir a uma autoridade distinta do produtor.
Quando usado, `autoridade_avaliacao` identifica quem decide. O prazo de
conservação continua obrigatório — nos sistemas em causa o prazo é legal e
conhecido mesmo quando a apreciação está pendente.

### 3.3 Perfis

`perfil` é um enum aberto com padrão `^([a-z]{2}-[a-z0-9-]+|generic)$`. Cada
perfil registado tem um schema em `specs/registry/profiles/<perfil>.schema.json`
que restringe o bloco `avaliacao` para essa jurisdição.

Criados nesta ronda:

- **`pt-dglab`** — mantém integralmente as regras atuais: `classificacao_ref` e
  `instrumento_ref` no formato `<instrumento>/<...>`, e a regra de
  correspondência de prefixo entre ambos (SPEC §3.2.2). **Zero regressão para a
  Administração Pública portuguesa.**
- **`generic`** — sem restrições jurisdicionais; `classificacao_ref` e
  `instrumento_ref` são strings não vazias.

O schema do perfil **DEVE viajar dentro do `.ndfpkg`**, em `schemas/`, pela
mesma razão e com o mesmo mecanismo dos schemas de tipo documental (ADR-014).

### 3.4 A linha que a abstração não atravessa

`prazo_conservacao` e `destino_final` permanecem **no core**, com estrutura
concreta e enums fechados. A alternativa — delegar o bloco inteiro ao schema do
perfil — foi rejeitada por falhar este teste:

> Um leitor que nunca ouviu falar do perfil declarado consegue, apenas com o
> NDF-core, responder a: *este documento é eliminável, e a partir de quando?*

Com a estrutura no core, sim. Com tudo delegado ao perfil, não — e perde-se
exatamente a gestão de retenção transversal a jurisdições que justifica a
generalização. **Abstrai-se o vocabulário; mantém-se a estrutura.**

Critério para qualquer generalização futura: só se abstrai um eixo quando for
possível **nomear três sistemas reais que divergem nesse eixo**. Para
`avaliacao` era possível (PT/FR convergem, NL diverge, DE diverge). Para um
mecanismo genérico de extensão de metadados não é — e por isso não se faz.

---

## 4. Desenho — separação custódia ↔ RGPD

### 4.1 Forma

```json
{
  "metadados": {
    "tipo_documento_ref": "oficio@1.0.0",
    "entidade_produtora": { "designacao": "Direção-Geral de Exemplo" },
    "entidade_responsavel": "Direção-Geral de Exemplo",
    "contem_dados_pessoais": true,
    "protecao_dados": {
      "categorias": ["identificacao_fiscal", "dados_processuais"],
      "base_legal_conservacao": "obrigacao_legal",
      "responsavel_tratamento": "Direção-Geral de Exemplo"
    }
  }
}
```

### 4.2 Regras

- **`entidade_responsavel`** — obrigatório sempre. Entidade responsável pela
  custódia do registo. É o conceito que a SPEC atual descreve mas aloja no campo
  errado.
- **`protecao_dados`** — obrigatório se e só se `contem_dados_pessoais: true`;
  **proibido** caso contrário. Agrupa os três campos que só têm significado
  quando há dados pessoais: `categorias` (era `categorias_dados_pessoais`),
  `base_legal_conservacao` e `responsavel_tratamento`.
- `contem_dados_pessoais` mantém-se obrigatório: a declaração explícita de
  ausência tem valor probatório e não é substituível por omissão do bloco.

O ganho verificável é a proibição: hoje um documento pode declarar responsável
pelo tratamento afirmando não conter dados pessoais, sem que nada o detete.

### 4.3 Fora de âmbito

Não se acrescenta contacto do encarregado de proteção de dados (EPD/DPO). Muda
ao longo do tempo e o NDF-core é imutável — cai no princípio de âmbito de
[`LACUNAS.md`](../../LACUNAS.md).

---

## 5. Versão

Ambas as alterações são incompatíveis. São absorvidas em **1.0.0**, não numa
2.0.0.

Fundamento: o NDF está em nível 1 — Draft, com revisão pública por abrir e sem
utilizadores externos. Publicar uma 1.0.0 sabidamente incompleta para a corrigir
depois numa 2.0.0 incompatível é o pior dos dois caminhos numa candidatura. O
custo da alteração é hoje o mais baixo que alguma vez será.

Implica: retirar o item de generalização de `avaliacao` de v2.0.0 no
`ROADMAP.md` e fechar R11 na `READINESS-ASSESSMENT.md`.

---

## 6. Explicitamente fora desta ronda

- **Perfis `fr-siaf`, `nl-na`, `de-bund`, `eu-crl`** — carecem de confirmação
  contra fonte primária (§2.1).
- **Separar transferência de conservação permanente** (§2, divergência 3) — não
  bloqueia nenhuma jurisdição; `conservacao_permanente` é interpretável em todas.
  Registar como questão aberta, não resolver por antecipação.
- **Chaves do NDF-core em inglês** — o core é integralmente português
  (`metadados`, `documento`, `relacoes`, `participantes`). Traduzir só
  `avaliacao` seria incoerente. A questão da língua é real para adoção externa,
  mas é a mesma questão do risco R3 (ausência de conteúdo em inglês) e tem de
  ser decidida para o conjunto, não para um bloco.
- **Alargar a generalização a outros blocos** — nenhum outro bloco falha o teste
  dos três sistemas.

---

## 7. Condição de aceitação

A generalização só é defensável com evidência executável. Requisitos:

1. Pelo menos **um caso de conformidade válido não-PT** (`perfil: "generic"`),
   incluindo o caminho `destino_final: "a_determinar"` — que modela o caso
   alemão de apreciação pendente.
2. Casos inválidos para as novas regras: `a_determinar` sem
   `autoridade_avaliacao`; `protecao_dados` presente com
   `contem_dados_pessoais: false`; `perfil` ausente.
3. As regras portuguesas continuam cobertas pelos casos inválidos existentes
   (`mismatched-instrument`, formato de `classificacao_ref`), agora sob o perfil
   `pt-dglab`.

Sem estes, "suporta os sistemas arquivísticos europeus" seria uma alegação sem
prova — o padrão que os riscos R2 e R6 já representam neste projeto.

---

## 8. Fontes do levantamento comparativo

- Nationaal Archief — MDTO, `waardering`: https://www.nationaalarchief.nl/archiveren/mdto/waardering
- Bundesarchiv — Aussonderung von Schriftgut aus der E-Akte Bund (V2.3, 2026-01-28)
- Durée d'utilité administrative (DUA) — definição e prática de *sort final*
- Council of Europe — User Guide to Retention and Disposal Schedules
- Comissão Europeia — política de gestão documental e arquivo (Common Retention List)
- eArchiving / E-ARK — especificações CITS ERMS
