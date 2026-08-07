# ADR-005: Proveniência essencial de IA no core; logs detalhados fora do NDF

**Estado**: Aceite
**Data**: 2026-08-07
**Decisores**: carloscanutocosta

---

## Contexto

Sistemas de IA podem intervir na produção de um documento NDF (redação,
resumo, classificação, tradução). O NORMORDIS pretende preservar evidência
dessa intervenção, incluindo o estado de revisão humana, de forma alinhada
com os objetivos de rastreabilidade e supervisão humana do Regulamento (UE)
2024/1689 (AI Act) — sem transformar o NDF num garante de conformidade
jurídica, que não lhe compete.

## Decisão

Dois níveis de evidência:

1. **Proveniência essencial**, no bloco opcional `proveniencia_ia` do
   NDF-core — coberta pela assinatura: finalidade, sistema/fornecedor/
   modelo/versão, resultado incorporado, segmentos afetados, estado de
   revisão humana.
2. **Logs detalhados** (prompts integrais, respostas completas), fora do
   NDF, sob política própria de acesso e retenção, ligados por
   `evidencia_ref` (identificador + hash).

## Alternativas consideradas

### Embutir prompts e respostas completas no NDF-core

**Prós**: evidência mais completa num único artefacto.

**Contras**: o NDF-core é potencialmente conservado por décadas (PCA/DF,
§3). Prompts e respostas de IA podem conter dados pessoais, informação
confidencial ou instruções internas — material desproporcionado para
conservação permanente e para o princípio de minimização (RGPD, Art.º 5.º,
n.º 1, al. c), já aplicado no NDF a outros campos — §2.8, §1.4). Rejeitado.

### Não incluir nada sobre IA no NDF-core, deixando tudo em sistemas externos

**Prós**: NDF-core mais simples; nenhuma decisão de schema a tomar agora.

**Contras**: sem qualquer campo no core, a evidência essencial (que houve
intervenção de IA, qual, e se foi revista) fica inteiramente dependente de
sistemas externos não cobertos pela assinatura — perde-se precisamente a
garantia de imutabilidade e verificabilidade que motiva o NDF. Rejeitado.

### `revisao_humana` opcional, omitido quando não há revisão

**Prós**: schema mais simples.

**Contras**: apagaria a distinção entre "ainda não revisto" e "revisão não
aplicável" — omitir o campo é indistinguível de esquecimento. Optou-se por
tornar `revisao_humana.estado` obrigatório, incluindo o valor `"pendente"`,
para que a ausência de revisão seja representável e visível.

## Justificação da decisão

A separação replica, no domínio de IA, a mesma lógica já aplicada a dados
pessoais no NDF (§1.4): o core preserva o mínimo estruturalmente necessário
para compreender e auditar; o detalhe potencialmente sensível ou
desproporcionado fica fora, sob controlo próprio, ligado por referência
verificável (hash).

## Consequências

**Positivas**: evidência de utilização de IA torna-se parte do documento
assinado, sem forçar inclusão de material sensível; estado de revisão humana
é sempre explícito, nunca implícito por omissão.

**Negativas / mitigações**: exige que sistemas produtores mantenham um
repositório externo de evidência detalhada quando aplicável — fora do
âmbito desta especificação, tal como já acontece para anexos binários
(§2.9.4).

## Referências

- SPEC.md §2.13
- `docs/normalization/AI-PROVENANCE-GUIDANCE.md`
- Regulamento (UE) 2024/1689 (AI Act) — referência informativa, não
  normativa para este ADR
