# Registo

Catálogo oficial de identificadores canónicos (`schema_id`) para o ecossistema NORMORDIS.

## Objetivo

- Evitar colisões entre identificadores de tipos de documento
- Garantir estabilidade dos `schema_id` ao longo do tempo
- Suportar versionamento de templates (`versao_ndt`)

## Formato de entrada

```json
{
  "schema_id": "modelo3-irs",
  "descricao": "Modelo 3 de IRS — Declaração de rendimentos",
  "emissor": "AT",
  "perfil": "impresso_complexo",
  "versoes": [
    { "versao_ndt": "2026.1", "referencia_legal": "Portaria n.º .../2026", "vigente": true }
  ]
}
```

## Perfis de avaliação arquivística

`profiles/` contém os schemas dos perfis referenciados por
`NDF-core.avaliacao.perfil` (NDF SPEC.md §3.2.3):

| Perfil | Âmbito |
|---|---|
| `pt-dglab` | Administração Pública portuguesa — MEG/DGLAB |
| `generic` | Sem restrições jurisdicionais |

## Entradas registadas

> A definir.
