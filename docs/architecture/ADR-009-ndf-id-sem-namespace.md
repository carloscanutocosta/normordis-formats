# ADR-009: `ndf_id` mantém-se um UUID v4 opaco, sem espaço de nomes por entidade

**Estado**: Aceite
**Data**: 2026-08-08
**Decisores**: carloscanutocosta

---

## Contexto

`LACUNAS.md` L6 apontava que `ndf_id` (UUID v4 puro) não distingue
visualmente a entidade produtora, e que nada impede — ainda que
improvável — colisão deliberada por um sistema produtor comprometido.
`ROADMAP.md` (item A10) tinha previsto isto como candidato a `v2.0.0`,
a resolver junto com "Extensões de namespace (`ext.<entidade>`)". Esta ADR
é a proposta dedicada que esse item exigia antes de qualquer alteração de
schema.

## Decisão

**Não alterar o formato de `ndf_id`.** Mantém-se UUID v4 puro
(RFC 9562), sem prefixo, sufixo ou componente estrutural que identifique a
entidade produtora. A atribuição a uma entidade produtora já é resolvida
por `metadados.entidade_produtora` (§2.7.3, com `designacao`, `nif`,
`codigo_dglab`) — campo estruturado, presente em todo o NDF-core, coberto
pela assinatura.

## Alternativas consideradas

### Prefixar o UUID com um código de entidade

Ex.: `PT-DGE-000:a1b2c3d4-e5f6-4789-abcd-ef0123456789`.

**Prós**: identificação visual imediata da entidade produtora a partir do
`ndf_id`.

**Contras — determinantes**:
- **Viola o princípio de desenho de identificadores opacos.** Um
  identificador que incorpora significado organizacional acopla a
  identidade permanente do documento à identidade, também mutável, da
  entidade que o produziu. Entidades da AP são reorganizadas, fundidas,
  extintas e renomeadas — um `ndf_id` com "DGE" embutido para sempre,
  produzido por uma entidade que 10 anos depois se chama outra coisa ou já
  não existe, fica com um prefixo permanentemente desatualizado, sem
  forma de corrigir sem violar a imutabilidade do identificador (§2.3).
- **Blast radius elevado para um problema já resolvido de outra forma**: a
  alteração tocaria `ndf_id` (ndf-core.schema.json), `versao_anterior`
  (envelope.schema.json), `manifest.schema.json`, `custody-event.schema.json`,
  `relacoes[].alvo.ndf_id` e campos análogos no registo
  (`despacho.sobre[].ndf_id`) — pelo menos seis ficheiros, para resolver um
  problema que `entidade_produtora` já resolve sem qualquer alteração.
- A informação que se pretendia obter (qual a entidade produtora) já
  existe, estruturada e assinada, em `metadados.entidade_produtora` — a
  motivação original da proposta.

### Espaço de endereçamento (probabilidade de colisão)

UUID v4 tem 122 bits de entropia — a probabilidade de colisão entre dois
`ndf_id` gerados independentemente é desprezável para qualquer volume
plausível de documentos da Administração Pública portuguesa, num cálculo
análogo ao já feito para `validation_code` (100 bits — SPEC.md §4.6.3, onde
10¹² documentos produzem probabilidade de colisão ≈ 3.9 × 10⁻⁷). Um
sistema produtor comprometido que gere `ndf_id` deliberadamente colidentes
é um cenário de ataque diferente — nenhum esquema de namespace no
identificador o impede, porque um atacante com essa capacidade também
pode falsificar o namespace. A mitigação real desse cenário é a cadeia de
custódia (§2.4.2) e a assinatura, não a estrutura do identificador.

## Justificação da decisão

A pergunta que a proposta original pretendia responder — "a que entidade
pertence este documento?" — já tem resposta estruturada, assinada e
imutável em `metadados.entidade_produtora`. Misturar essa resposta dentro
do próprio identificador não acrescenta capacidade nova, introduz uma
alteração de grande alcance em seis ficheiros de schema, e cria um risco
concreto (desalinhamento permanente entre o prefixo e a realidade
organizacional) sem benefício correspondente.

Fecha-se assim a lacuna identificada em `LACUNAS.md` L6 por **clarificação
normativa**, não por alteração de schema — o mesmo padrão já seguido para
L7, L8, L9 e L10 nesta mesma revisão.

## Consequências

**Positivas**: nenhuma alteração de schema; nenhum risco de compatibilidade;
`ndf_id` mantém-se um identificador simples, opaco e já testado.

**Negativas / mitigações**: quem quiser identificar visualmente a entidade
produtora a partir de um `ndf_id` isolado não o consegue — tem de consultar
`metadados.entidade_produtora` (ou o portal de verificação, §4.6.4).
Aceite: não é uma capacidade que o identificador deva fornecer.

**Nota sobre "Extensões de namespace" (roadmap `v2.0.0`)**: este item do
roadmap ("`ext.<entidade>`") mantém-se relevante para extensão do
NDF-core por campos próprios de uma entidade (ex.: `ext.at.campo_x` dentro
de `documento` ou `metadados`) — um problema genuinamente distinto de
namespacing de `ndf_id`. Já parcialmente antecipado, para `relacoes[].tipo`
especificamente, pelo mecanismo de extensão qualificada da ADR-008.

## Referências

- SPEC.md §2.3, §2.7.3, §4.6.3
- `LACUNAS.md` L6
- ADR-008-extensao-qualificada-relacoes.md
