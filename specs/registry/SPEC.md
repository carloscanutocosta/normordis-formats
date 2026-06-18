# NORMORDIS Registry — Tipos de Documento

**Versão**: 1.0.0  
**Estado**: Draft para implementação

---

## 1. Propósito

O registry define o mecanismo de resolução de `tipo_documento_ref` — o campo do NDF-core que identifica o schema da estrutura interna de `documento`. Cada entrada do registry é um schema JSON (JSON Schema Draft 2020-12) que valida o conteúdo de `documento` para um tipo específico.

---

## 2. Formato do identificador

```
<id>@<versao>
```

| Componente | Regras | Exemplos |
|---|---|---|
| `id` | Lowercase, hífens, sem espaços; estável (não muda com versões) | `oficio`, `informacao-tecnica`, `despacho`, `modelo3-irs` |
| `versao` | SemVer 2.0.0 para tipos normativos; `YYYY.N` para impressos com versão anual | `1.0.0`, `2026.1` |

---

## 3. Tipos canónicos (esta especificação)

| `tipo_documento_ref` | Descrição | Schema |
|---|---|---|
| `oficio@1.0.0` | Ofício — comunicação formal externa | [schemas/oficio.schema.json](schemas/oficio.schema.json) |
| `informacao-tecnica@1.0.0` | Informação técnica — nota interna fundamentada | [schemas/informacao-tecnica.schema.json](schemas/informacao-tecnica.schema.json) |
| `despacho@1.0.0` | Despacho — decisão ou instrução de serviço | [schemas/despacho.schema.json](schemas/despacho.schema.json) |

Tipos específicos de cada entidade (AT, SS, Municípios, etc.) são definidos fora desta especificação base mas seguem o mesmo formato de schema.

---

## 4. Resolução

Um leitor NDF resolve `tipo_documento_ref` na seguinte ordem de precedência:

1. **`.ndfpkg`**: se presente no pacote de exportação, o schema fica em `registry/<tipo_documento_ref>.schema.json` dentro do ZIP.
2. **Registry local**: implementação mantém uma cópia local dos schemas canónicos.
3. **Registry remoto** (roadmap): URI canónico `https://registry.normordis.pt/<id>/<versao>/schema.json`.

---

## 5. Compatibilidade

Segue as mesmas regras SemVer da especificação NDF (§7):
- `MINOR`: adição de campos opcionais — leitores antigos ignoram.
- `MAJOR`: mudança incompatível — leitores recusam processar.

Um NDF que declare `tipo_documento_ref: "oficio@1.0.0"` é válido para qualquer leitor que suporte `oficio@1.x.x`.
