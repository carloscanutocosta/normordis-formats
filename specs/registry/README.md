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

**Nota de estado (Fase 1E, P0.1)**: `pt-dglab` é um perfil **experimental do
projeto NORMORDIS**, não uma adoção ou homologação do modelo MEG/DGLAB pela
Direção-Geral do Livro, dos Arquivos e das Bibliotecas ou por qualquer outra
entidade da Administração Pública portuguesa. A mesma nota consta da
`description` do próprio schema
([`profiles/pt-dglab.schema.json`](profiles/pt-dglab.schema.json)), para
quem consome apenas o schema sem ler este README.

## Entradas registadas

> A definir.
