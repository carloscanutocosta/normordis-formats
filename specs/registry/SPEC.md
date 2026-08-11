# Registo NORMORDIS — Tipos de documento

**Versão**: 1.0.0  
**Estado**: Draft — revisão pública por abrir

---

## 1. Propósito

O registo define o mecanismo de resolução de `tipo_documento_ref` — o campo do NDF-core que identifica o schema da estrutura interna de `documento`. Cada entrada do registo é um schema JSON (JSON Schema Draft 2020-12) que valida o conteúdo de `documento` para um tipo específico.

---

## 2. Formato do identificador

```
<id>@<versao>
```

| Componente | Regras | Exemplos |
|---|---|---|
| `id` | Lowercase, hífens, sem espaços; estável (não muda com versões) | `oficio`, `informacao-tecnica`, `despacho`, `parecer`, `modelo3-irs` |
| `versao` | SemVer 2.0.0 para tipos normativos; `YYYY.N` para impressos com versão anual | `1.0.0`, `2026.1` |

---

## 3. Tipos canónicos (esta especificação)

| `tipo_documento_ref` | Descrição | Schema |
|---|---|---|
| `oficio@1.0.0` | Ofício — comunicação formal externa | [schemas/oficio.schema.json](schemas/oficio.schema.json) |
| `informacao-tecnica@1.0.0` | Informação técnica — nota interna fundamentada | [schemas/informacao-tecnica.schema.json](schemas/informacao-tecnica.schema.json) |
| `parecer@1.0.0` | Parecer — apreciação fundamentada com sentido explícito, sobre outro documento | [schemas/parecer.schema.json](schemas/parecer.schema.json) |
| `despacho@1.0.0` | Despacho — decisão ou instrução de serviço | [schemas/despacho.schema.json](schemas/despacho.schema.json) |

`informacao-tecnica`, `parecer` e `despacho` formam, em conjunto com
`NDF-core.relacoes` (SPEC.md §2.11), a cadeia documental
Informação → Parecer → Despacho — três documentos NDF autónomos ligados por
relações verificáveis, nunca um único documento com secções sucessivamente
assinadas. Ver exemplo em `specs/ndf/examples/informacao-parecer-despacho/`.

Tipos específicos de cada entidade (AT, SS, Municípios, etc.) são definidos fora desta especificação base mas seguem o mesmo formato de schema.

---

## 4. Resolução

Um leitor NDF resolve `tipo_documento_ref` na seguinte ordem de precedência:

1. **`.ndfpkg`**: se presente no pacote de exportação, o schema fica em `registry/<tipo_documento_ref>.schema.json` dentro do ZIP.
2. **Registo local**: implementação mantém uma cópia local dos schemas canónicos.
3. **Registo remoto** (roadmap): URI canónico `https://registry.normordis.pt/<id>/<versao>/schema.json`.

---

## 5. Compatibilidade

Segue as mesmas regras SemVer da especificação NDF (§7):
- `MINOR`: adição de campos opcionais; leitores antigos podem preservar o
  objeto como opaco ou recusá-lo, mas não ignoram silenciosamente conteúdo
  assinado desconhecido.
- `MAJOR`: mudança incompatível — leitores recusam processar.

Um leitor só declara interpretação completa das versões que suporta
explicitamente.
