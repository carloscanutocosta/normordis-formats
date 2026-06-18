# Especificação NCRTF

**NORMORDIS Canonical Rich Text Format**

Estado: Pendente — especificação a desenvolver.

## Âmbito

Formato canónico de conteúdo rico, independente de HTML, DOCX e PDF.

## Representa

- Texto estruturado
- Listas
- Tabelas
- Imagens
- Referências documentais
- Semântica editorial

## Não representa

- O documento jurídico completo (isso é o NDF)
- Regras de validação ou cálculo (isso é o NDT)
- Layout de página (isso é o bloco `layout` do NDT)

## Relação com outros formatos

```
NCRTF
  ↓ (renderizado por)
NDT [bloco layout]
  ↓
PDF/A | HTML | ...
```

## Próximos passos

- Definir estrutura base (blocos de conteúdo, inline markers)
- Definir serialização canónica (JSON, alinhada com JCS/RFC 8785)
- Definir JSON Schema
- Criar exemplos
