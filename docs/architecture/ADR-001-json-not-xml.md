# ADR-001: JSON como formato de serialização do NDF-core

**Estado**: Aceite  
**Data**: 2026-06-18  
**Decisores**: carloscanutocosta

---

## Contexto

O NDF-core é o objecto canónico de armazenamento do documento institucional — é o que é canonicalizado, assinado e preservado. A escolha do formato de serialização afecta directamente:

- a canonicalização determinística (requisito de assinatura)
- a eficiência de armazenamento em base de dados
- a complexidade de implementação para terceiros
- a interoperabilidade com ecossistemas externos

Os candidatos avaliados foram: **JSON**, **XML**, **CBOR** e **Protocol Buffers**.

---

## Decisão

**O NDF-core é serializado em JSON**, estrito e canonicalizado via JCS (JSON Canonicalization Scheme, RFC 8785).

---

## Alternativas consideradas

### XML

**Prós**:
- Formato histórico da Administração Pública portuguesa e europeia (SAFT-PT, UBL, xADES)
- Esquemas de validação maduros (XSD, RelaxNG)
- Suporte nativo a namespaces para extensibilidade institucional

**Contras**:
- Não existe um standard de canonicalização XML adequado para assinatura de documentos de arquivo com a robustez do RFC 8785. XML Canonical (C14N, W3C) tem ambiguidades conhecidas e implementações divergentes.
- XAdES (assinatura XML) é substancialmente mais complexo de implementar correctamente do que CAdES sobre JSON canonicalizado.
- Armazenamento nativo em base de dados relacional: o tipo `xml` do PostgreSQL tem performance inferior ao `jsonb` para queries estruturadas. Não há equivalente ao `jsonb` para XML.
- Verbosidade: os mesmos dados estruturados ocupam tipicamente 30–60% mais espaço em XML do que em JSON.
- A interoperabilidade XML com sistemas externos (SAFT-PT, UBL, eIDAS de outros EM) é resolvida por **adapters de exportação** — o NDF-core não é o formato de troca directo. Esta separação é intencional.

### CBOR (RFC 7049 / RFC 8949)

**Prós**:
- Binário, muito compacto
- Suporte a canonicalização (RFC 8949, §4.2)
- Desenhado para ambientes IoT/constrangidos

**Contras**:
- Não é human-readable — inspecção directa de um documento de arquivo requer ferramentas de decode
- Ecossistema de tooling significativamente menor do que JSON
- Não é adequado para `jsonb` em PostgreSQL
- A adopção na Administração Pública e nos sistemas de arquivo europeus é negligenciável

### Protocol Buffers (protobuf)

**Prós**:
- Muito compacto e eficiente
- Schema fortemente tipado

**Contras**:
- Formato proprietário (Google); não é um standard aberto
- Não tem canonicalização determinística formal adequada para assinatura jurídica
- Não é human-readable
- Incompatível com os objectivos de formato aberto e independência de fornecedor do normordis-spec

---

## Justificação da decisão

### 1. Canonicalização determinística robusta

O RFC 8785 (JSON Canonicalization Scheme) define uma canonicalização estrita de JSON que produz os mesmos bytes para a mesma estrutura lógica, independentemente da ordem de inserção de chaves, formatação, ou implementação. Esta propriedade é necessária para que a assinatura CAdES sobre `sha256(payload_bytes)` seja verificável por qualquer implementação conforme.

Não existe equivalente XML com o mesmo nível de robustez e adopção. C14N (W3C XML Canonical) tem ambiguidades documentadas que produzem resultados diferentes em implementações distintas.

### 2. Armazenamento em base de dados relacional

O PostgreSQL oferece o tipo `jsonb` que permite:
- indexação nativa de campos internos sem parse externo
- queries estruturadas com operadores JSON nativos
- geração de colunas computadas a partir do conteúdo JSON

Não existe equivalente para XML com a mesma performance e expressividade de query. Isto é relevante para o modelo de armazenamento do NDF (§1.5 da spec NDF).

### 3. Simplicidade de implementação para terceiros

O objectivo central do normordis-spec é que qualquer fornecedor possa implementar leitura e escrita de NDF sem dependência das bibliotecas de referência. JSON tem parsers disponíveis em todas as linguagens e plataformas sem dependências externas. XML requer parsers mais complexos e a validação XSD/RelaxNG exige bibliotecas adicionais.

### 4. Separação entre formato interno e formato de troca

O NDF-core é o formato de **armazenamento interno**. Interoperabilidade XML com sistemas externos (SAFT-PT, UBL, eIDAS de outros Estados-Membros, SIARQ, etc.) é resolvida por **adapters de exportação** fora do âmbito desta especificação. O NDF-core é a fonte de verdade a partir da qual essas exportações são derivadas.

Esta separação permite que o formato interno seja optimizado para arquivo, integridade e eficiência de DB, enquanto os formatos de troca são optimizados para os requisitos específicos de cada integração.

---

## Consequências

**Positivas**:
- Canonicalização robusta via RFC 8785 — base segura para assinatura CAdES
- Armazenamento eficiente com `jsonb` no PostgreSQL
- Implementação acessível a qualquer fornecedor sem tooling especializado
- Human-readable — um documento NDF pode ser inspeccionado directamente num editor de texto

**Negativas / mitigações**:
- Interoperabilidade XML com sistemas externos requer adapters de exportação → resolvido por `normordis-pdf` e futuros adaptadores (fora do âmbito desta spec)
- JSON não tem suporte nativo a tipos binários → resolvido por referência por hash para recursos externos; dados binários nunca são embebidos no NDF-core

---

## Referências

- RFC 8785 — JSON Canonicalization Scheme (JCS)
- RFC 8949 — Concise Binary Object Representation (CBOR) — considerado e rejeitado
- W3C XML C14N — Canonical XML — considerado e rejeitado
- ETSI EN 319 122 — CAdES (aplicado sobre JSON canonicalizado)
- PostgreSQL JSONB documentation
