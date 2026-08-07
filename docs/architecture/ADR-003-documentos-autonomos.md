# ADR-003: Documentos autónomos em vez de secções sucessivamente assinadas

**Estado**: Aceite
**Data**: 2026-08-07
**Decisores**: carloscanutocosta

---

## Contexto

Um procedimento administrativo comum — informação técnica, parecer, despacho
— pode ser modelado de duas formas fundamentalmente distintas:

1. Como um único NDF que acumula secções (informação, depois parecer, depois
   despacho) e é sucessivamente assinado por diferentes intervenientes.
2. Como três NDF autónomos e independentes, cada um com o seu próprio
   `ndf_id`, conteúdo, avaliação arquivística e assinatura(s), ligados por
   relações verificáveis (ADR-002).

## Decisão

Adotar o modelo 2. Informação, parecer e despacho são documentos autónomos.
`relacoes[]` (ADR-002) é o mecanismo que os liga.

## Alternativas consideradas

### Um único NDF com secções sucessivamente assinadas

**Prós**: um único `ndf_id`, um único ficheiro, potencialmente mais simples
de armazenar e transportar.

**Contras**: não corresponde à realidade administrativa nem jurídica. Uma
informação técnica, um parecer e um despacho têm autoria, responsabilidade,
avaliação arquivística e — frequentemente — regime de assinatura distintos
(§2.10). Tratá-los como o mesmo documento obrigaria a decisões arbitrárias:
qual o `nivel_assinatura` do conjunto? Qual `tipo_documento_ref`? O que
acontece se o parecer for desfavorável e o despacho decidir em sentido
contrário — isso é uma "alteração" do mesmo documento, violando a
imutabilidade (§2.1)? Nenhuma resposta é satisfatória, porque a premissa
está errada: não são o mesmo documento.

## Justificação da decisão

- Cada documento tem autoria, responsabilidade e avaliação arquivística
  (PCA/DF) próprias — mesmo quando tramitados juntos, um parecer pode ter um
  prazo de conservação diferente do despacho que o aprecia.
- Um despacho pode decidir com base em múltiplos antecedentes (uma
  informação e mais do que um parecer) — um modelo de secções sucessivas não
  representa naturalmente múltiplos antecedentes independentes; um modelo de
  relações representa-o diretamente (`relacoes[]` é um array).
- É mais fiel ao princípio de imutabilidade: cada documento é finalizado e
  assinado uma vez; o "avanço" do procedimento cria novos documentos, nunca
  edita os anteriores.

## Consequências

**Positivas**: modelo mais próximo da prática administrativa real; permite
antecedentes múltiplos; não força decisões arbitrárias de âmbito.

**Negativas / mitigações**: mais ficheiros a gerir por procedimento —
mitigado pelo facto de o sistema de custódia já trabalhar ao nível do NDF
individual, e pelo grafo de relações tornar a reconstrução do procedimento
completo trivial para um leitor conforme.

## Referências

- SPEC.md §2.11 (relações), §3 (avaliação arquivística por documento)
- ADR-002-relacoes-no-core.md
- `specs/ndf/examples/informacao-parecer-despacho/`
