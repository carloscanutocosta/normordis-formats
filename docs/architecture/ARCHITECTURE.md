# NORMORDIS — Arquitetura normativa comum

**Estado:** Draft normativo  
**Aplicável a:** NDF 1.x, NDT 2.x e NCRTF 2.x

## 1. Princípio

O documento lógico é a fonte de verdade. Uma representação PDF, ODF, HTML ou
futura é uma projecção desse documento e não substitui os dados de origem.

As especificações são agnósticas de linguagem, runtime, base de dados e
fornecedor. JSON Schema, algoritmos publicados, bytes esperados e vectores de
conformidade constituem o contrato. Ferramentas em Python ou qualquer outra
linguagem são implementações de referência substituíveis e nunca requisitos
normativos.

```text
editor ──► NCRTF ──┐
                   ├──► NDF-core ──┐
dados/metadados ───┘               ├──► renderer ──► PDF / ODF / HTML / …
                                   │
NDT + recursos ────────────────────┘

NDF-core + envelope + NDT + schemas + recursos ──► .ndfpkg
```

## 2. Responsabilidades

### 2.1 NDF

O NDF representa uma instância documental finalizada. Contém os dados,
metadados e conteúdo lógico que permitem compreender o documento, bem como os
elementos necessários para verificar a sua integridade e, quando aplicável, a
sua autenticidade.

O NDF divide-se em:

- **NDF-core**: JSON canónico e imutável, incluindo dados, metadados, avaliação
  arquivística, conteúdo NCRTF e a referência exacta ao NDT;
- **envelope**: hash do NDF-core, código de verificação, assinaturas ou selos
  opcionais, timestamps e material de validação;
- **registo de custódia**: eventos append-only relativos a ingestão, acesso,
  transições de estado, re-selagem e eliminação;
- **`.ndfpkg`**: representação portátil e autocontida, contendo NDF-core,
  envelope, NDT, schemas e recursos necessários para interpretar, verificar e
  renderizar o documento.

### 2.2 NDT

O NDT é um template declarativo de apresentação. Não contém dados de negócio,
não valida o NDF e não calcula valores. Os seus caminhos de dados são sempre
relativos a `NDF-core.documento`.

Um NDT pode orientar múltiplos formatos de saída. Requisitos específicos de
PDF, ODF ou HTML pertencem a perfis de renderer, não ao modelo lógico NDT.

### 2.3 NCRTF

O NCRTF é a representação canónica de rich text incorporada como valor JSON no
NDF-core. É independente do editor de origem. Lexical, Quill, ProseMirror ou
outros editores são adaptadores de entrada e saída, não formatos persistentes
normativos.

## 3. Integridade, imutabilidade e autenticidade

Estes conceitos não são sinónimos:

- **integridade**: uma alteração dos bytes canónicos é detectável;
- **imutabilidade de custódia**: o sistema impede substituição silenciosa e
  regista qualquer evento posterior à finalização;
- **autenticidade**: a identidade ou autoridade do emissor pode ser validada
  contra uma âncora de confiança;
- **assinatura qualificada**: nível jurídico específico, exigido apenas quando
  a natureza do acto ou a lei aplicável o determinar.

Todo o NDF finalizado DEVE ter NDF-core canonicalizado por JCS, `payload_hash`
SHA-256 e armazenamento append-only ou WORM com log de auditoria. Um hash sem
uma âncora de custódia permite detectar alterações face a uma cópia conhecida,
mas não impede que um atacante substitua simultaneamente conteúdo e hash.

CAdES NÃO É obrigatório para todos os documentos. Aplicam-se os seguintes
perfis:

| Perfil | Requisito | Uso típico |
|---|---|---|
| `integridade` | JCS + hash + custódia append-only/WORM + auditoria | registos internos sem acto assinável |
| `selo_institucional` | perfil `integridade` + selo electrónico CAdES da entidade | prova portátil de origem e integridade institucional |
| `assinatura_avancada` | perfil `integridade` + assinatura CAdES avançada | actos que exigem identificação do signatário |
| `assinatura_qualificada` | perfil `integridade` + assinatura CAdES qualificada | actos para os quais a lei ou política exige assinatura qualificada |

O campo `nivel_assinatura` do NDF-core declara o requisito jurídico de
assinatura pessoal (`nenhuma`, `avancada` ou `qualificada`). Um documento com
`nivel_assinatura: "nenhuma"` pode, opcionalmente, receber selo institucional;
o selo não transforma o documento numa assinatura pessoal.

Quando `nivel_assinatura` for `"avancada"` ou `"qualificada"`, a assinatura
CAdES original é parte inseparável do registo arquivístico. O custodiante DEVE
preservar, sem alteração ou substituição, os bytes DER originais do contentor
CAdES, os timestamps e o material de validação capturado. Esta obrigação
mantém-se durante todo o prazo de conservação e enquanto o NDF-core for
preservado. Renovações, novos timestamps ou migrações criptográficas são novas
provas append-only e nunca reescrevem a assinatura original.

O `validation_code` é aposto à representação visual como chave pública de
consulta. Isoladamente, relaciona o código com um NDF; quando consultado no
portal público oficial, permite ao custodiante confirmar a autenticidade
institucional do documento, o seu hash, entidade produtora e estado corrente.
Fora do portal, a autenticidade depende de assinatura/selo verificável ou de
outra âncora de custódia confiável.

## 4. Eficiência e autocontenção

Existem duas representações conformes:

- **perfil de custódia**: armazenamento em base de dados do NDF-core canónico e
  envelope; NDTs, schemas, certificados e recursos podem ser deduplicados por
  hash dentro do domínio de custódia, desde que a resolução seja transaccional,
  imutável e auditável;
- **perfil portátil**: `.ndfpkg` sem dependências externas, no qual todos os
  objectos referenciados são materializados e inventariados por hash.

A deduplicação é uma optimização física e nunca altera o modelo lógico. Uma
exportação portátil DEVE reconstituir todos os objectos necessários.

## 5. Regras de integração

1. `NDF-core.ndt_version_ref` DEVE corresponder a `NDT.schema_id` e
   `NDT.versao_ndt`.
2. O `.ndfpkg` DEVE incluir esse NDT exacto e o respectivo hash no manifesto.
3. `metadados.tipo_documento_ref` DEVE resolver para o schema usado para validar
   `NDF-core.documento`.
4. Um caminho NDT `a.b.c` resolve para `NDF-core.documento.a.b.c`.
5. Um valor NCRTF no NDF-core DEVE validar contra a versão NCRTF declarada e
   cumprir as regras de canonicalização dessa versão.
6. Recursos NDT e NCRTF DEVE(M) resolver dentro do pacote ou do domínio de
   custódia e DEVEM ser verificados por hash antes de uso.
7. A ausência de um NDT não impede a leitura dos dados NDF, mas impede declarar
   uma renderização como reprodutível.

## 6. Ordem de verificação

Um verificador DEVE, pela ordem seguinte:

1. validar o manifesto e impedir caminhos absolutos ou com `..`;
2. verificar os hashes de todos os ficheiros inventariados;
3. validar NDF-core e envelope contra os schemas da versão declarada;
4. recalcular JCS, `payload_hash` e `validation_code`;
5. resolver e validar o schema de `tipo_documento_ref`;
6. validar todos os valores NCRTF;
7. validar assinaturas, selos, timestamps e cadeia de confiança, se presentes;
8. confirmar a correspondência entre `ndt_version_ref` e o NDT incluído.

Quando a assinatura for juridicamente obrigatória, a ausência ou alteração de
qualquer byte da assinatura original, timestamp ou material de validação DEVE
produzir resultado de verificação inválido, ainda que o NDF-core permaneça
íntegro.

Sem assinatura ou selo válido, o resultado DEVE ser descrito como **íntegro sob
a custódia avaliada**, e não como autenticamente emitido por uma identidade
criptograficamente comprovada.
