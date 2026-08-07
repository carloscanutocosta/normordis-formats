# ADR-002: Relações documentais assinadas no NDF-core

**Estado**: Aceite
**Data**: 2026-08-07
**Decisores**: carloscanutocosta

---

## Contexto

Um procedimento administrativo é tipicamente composto por vários documentos
relacionados — uma informação técnica, um ou mais pareceres, um despacho.
Antes desta decisão, a única relação entre NDF modelada formalmente era a
cadeia linear de substituição de versões (`versao_anterior`/`hash_anterior`),
e vivia inteiramente no **envelope**, fora dos bytes canonicalizados e
assinados. Não existia mecanismo genérico para representar que um parecer
incide sobre uma informação, ou que um despacho decide sobre um parecer,
exceto campos específicos de um único tipo de documento do registo
(`despacho.documento.sobre[]`), sem `payload_hash` — apenas `ndf_id`.

## Decisão

Introduzir um bloco opcional `relacoes` no **NDF-core**, com um vocabulário
fechado de tipos de relação (`substitui`, `corrige`, `complementa`, `anula`,
`responde_a`, `emite_parecer_sobre`, `decide_sobre`, `executa`, `anexa`,
`deriva_de`, `referencia`). Cada relação identifica o alvo por `ndf_id` **e**
`payload_hash` — nunca apenas pelo primeiro.

## Alternativas consideradas

### Manter as relações apenas no envelope

**Prós**: não exige nova versão de schema do core; não requer decisão sobre
versionamento.

**Contras**: a relação deixa de estar coberta pela assinatura — um
verificador não consegue confirmar que a relação declarada corresponde ao
que o signatário efetivamente assinou. Para uma relação com efeito
jurídico-documental (ex.: "este despacho decide sobre este parecer"), isso é
uma fragilidade inaceitável: a ligação entre documentos é parte do sentido
do ato, não um metadado operacional acessório.

### Vocabulário de relação como string livre, sem enum fechado

**Prós**: extensibilidade sem necessidade de nova versão da especificação.

**Contras**: o resto do NDF-core usa sistematicamente enums fechados para
vocabulário controlado (`classificacao_seguranca`, `destino_final`,
`nivel_assinatura`) e resolve extensibilidade por versão minor. Uma exceção
aqui introduziria um padrão de extensibilidade inconsistente sem benefício
demonstrado — nenhum caso de uso concreto exigia um valor fora do conjunto
inicial de 11.

### Referenciar apenas por `ndf_id`, sem `payload_hash`

**Prós**: mais simples; é o que `despacho.sobre[]` já fazia.

**Contras**: uma referência só por `ndf_id` identifica uma identidade
lógica, não um conteúdo imutável específico — não distingue "o parecer
incidiu sobre a versão X da informação" de "a informação foi entretanto
substituída". `payload_hash` no alvo torna a relação verificável contra os
bytes canónicos exatos existentes no momento em que foi estabelecida.

## Justificação da decisão

1. **Coerência com o princípio de imutabilidade** (SPEC.md §2.1): se o
   conteúdo é imutável e assinado, as relações que dão sentido documental ao
   conjunto de um procedimento administrativo devem ter a mesma garantia.
2. **Verificabilidade forte**: `alvo.payload_hash` permite a qualquer
   verificador confirmar exatamente que conteúdo foi apreciado, sem depender
   de o documento alvo permanecer inalterado ou de o sistema de custódia ser
   confiável para essa afirmação.
3. **Consistência de vocabulário controlado**: o enum fechado de `tipo`
   segue o mesmo padrão já estabelecido para outros campos normativos do
   NDF-core.

## Reconciliação com `despacho.sobre[]`

`despacho.sobre[]` não foi removido nem descontinuado — ganhou um campo
opcional `payload_hash` para poder ficar coerente com `relacoes[]` quando
ambos estiverem presentes. `relacoes[]` é a fonte de verdade genérica;
`sobre[]` mantém-se como campo de conveniência de leitura específico deste
tipo de documento. Ver SPEC.md §2.11.4.

## Consequências

**Positivas**:
- Relações documentais tornam-se parte do grafo verificável, cobertas pela
  mesma assinatura que protege o conteúdo.
- Vocabulário mapeável a PROV-O (informativo,
  `docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`) para interoperabilidade
  semântica fora do NORMORDIS.

**Negativas / mitigações**:
- Redundância potencial entre `relacoes[]` e `despacho.sobre[]` quando ambos
  presentes — mitigada por regra de coerência documentada, não imposta por
  validação cruzada de schema (ficaria acoplado ao registo de tipos de
  documento, fora do âmbito do NDF-core).
- Enum fechado limita relações não previstas — mitigado por extensão via
  nova versão minor, consistente com o resto da especificação.

## Referências

- SPEC.md §2.11
- `docs/design/NDF-STABILIZATION-PROPOSAL.md` §2
- `docs/normalization/NDF-INFORMATIVE-GUIDANCE.md` — mapeamento PROV-O
