# Orientações informativas — Proveniência de IA no NDF

**Estado:** informativo — não constitui requisitos NDF. Os requisitos
normativos do bloco `proveniencia_ia` estão em `specs/ndf/SPEC.md` §2.13.

## Objetivo

Este documento explica **como preencher** `proveniencia_ia` de forma
proporcional, e **o que esse preenchimento não significa**. Não substitui
avaliação jurídica própria sobre o Regulamento (UE) 2024/1689 (AI Act) ou
qualquer outro regime aplicável.

## O que o NDF garante e o que não garante

O NDF fornece mecanismos técnicos que podem apoiar rastreabilidade,
transparência, supervisão humana e conservação de evidências relativas ao
uso de sistemas de IA. **Não garante, por si só, conformidade com o AI Act**
— a conformidade depende do sistema de IA em causa, da sua finalidade,
classificação de risco, dos operadores envolvidos, do contexto jurídico e
das medidas técnicas e organizativas efetivamente aplicadas pela entidade
responsável. Um NDF com `proveniencia_ia` bem preenchido é **evidência** que
uma organização pode usar para apoiar uma demonstração de conformidade — não
é, em si mesmo, essa conformidade.

Evitar, em qualquer comunicação sobre o NDF, formulações como "garante
conformidade com o AI Act", "cumpre automaticamente" o Regulamento, ou "prova
conformidade jurídica". O padrão de redação correto está em SPEC.md §2.13.1.

## Minimização

Prompts integrais, respostas completas do sistema de IA, e documentos
submetidos ao modelo **não devem** ser incluídos no NDF-core. Podem conter
dados pessoais, informação confidencial, segredos institucionais ou material
desproporcionado para conservação permanente — o NDF-core é potencialmente
conservado por décadas (§3, PCA/DF), e nem todo o material usado para
produzir um documento tem esse horizonte de conservação.

Quando existir necessidade de preservar essa evidência mais detalhada,
guardá-la fora do NDF, sob política própria de controlo de acesso e
retenção, e referenciá-la a partir de `evidencia_ref` (identificador + hash)
— nunca embutida diretamente.

## Diferença entre autoria humana e assistência por IA

`proveniencia_ia` regista **que** um sistema de IA interveio e **como** —
não substitui a atribuição de autoria em `participantes` (SPEC.md §2.12). Um
documento redigido com apoio de IA e revisto por um humano continua a ter
esse humano como autor em `participantes`; a IA aparece apenas como sistema
interveniente em `proveniencia_ia.intervencoes[].sistema`, nunca como
`participante` com papel de autor, aprovador ou decisor (§2.13.4).

## Revisão humana — porque `"pendente"` é um valor válido e útil

`revisao_humana.estado` é obrigatório em cada intervenção, incluindo o valor
`"pendente"`. Isto é deliberado: se a ausência de revisão pudesse ser
representada simplesmente pela omissão do campo, o princípio Human-in-the-
Loop ficaria sem peso técnico — não haveria forma de distinguir "ainda não
revisto" de "não se aplica revisão a este caso". Um sistema que produz
rascunhos com apoio de IA e ainda não os submeteu a revisão humana DEVE
registar `estado: "pendente"`, não omitir `revisao_humana`.

## Exemplos de preenchimento

### Mínimo — IA não utilizada

```json
{ "proveniencia_ia": { "utilizada": false } }
```

### Intervenção pendente de revisão

```json
{
  "proveniencia_ia": {
    "utilizada": true,
    "intervencoes": [
      {
        "intervencao_id": "d4e5f6a7-b8c9-4012-def0-123456789012",
        "finalidade": "apoio_redacao",
        "sistema": { "nome": "assistente-redacao-interno", "fornecedor": "NORMORDIS Lab" },
        "executada_em": "2026-08-01T09:00:00Z",
        "resultado_incorporado": "parcialmente",
        "revisao_humana": { "estado": "pendente" }
      }
    ]
  }
}
```

### Completo — revisto e aprovado, com evidência externa

```json
{
  "proveniencia_ia": {
    "utilizada": true,
    "intervencoes": [
      {
        "intervencao_id": "e5f6a7b8-c9d0-4123-ef01-234567890123",
        "finalidade": "resumo",
        "sistema": { "nome": "assistente-redacao-interno", "fornecedor": "NORMORDIS Lab", "modelo": "modelo-x", "versao": "2026.7" },
        "executada_em": "2026-08-01T09:00:00Z",
        "resultado_incorporado": "parcialmente",
        "segmentos_afetados": ["documento.corpo"],
        "revisao_humana": {
          "estado": "revisto_com_alteracoes",
          "revisor_ref": "user:789",
          "revisto_em": "2026-08-01T14:00:00Z"
        },
        "evidencia_ref": {
          "tipo": "registo_externo",
          "identificador": "log-ia-2026-08-01-00042",
          "hash": "sha256:2b1c9a3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d"
        }
      }
    ]
  }
}
```

## Ver também

- `specs/ndf/SPEC.md` §2.13 — requisitos normativos.
- `docs/normalization/NDF-INFORMATIVE-GUIDANCE.md` — mapeamento jurídico
  geral e vocabulário de relações.
