# NORMORDIS — Arquitetura normativa comum

**Estado:** Draft — Revisão pública
**Aplicável a:** NDF 1.x, NDT 2.x e NCRTF 2.x

## 1. Princípio

O documento lógico é a fonte de verdade. Uma representação PDF, ODF, HTML ou
futura é uma projeção desse documento e não substitui os dados de origem.

O conjunto tem dois objetivos inseparáveis: armazenamento canónico, imutável,
autocontido e eficiente; e interoperabilidade entre sistemas independentes.

As especificações são agnósticas de linguagem, runtime, base de dados e
fornecedor. JSON Schema, algoritmos publicados, bytes esperados e vetores de
conformidade constituem o contrato. Ferramentas em Python ou qualquer outra
linguagem são implementações de referência substituíveis e nunca requisitos
normativos.

```text
editor ──► NCRTF ──┐
                   ├──► NDF-core ──┐
dados/metadados ───┘               ├──► renderizador ──► PDF / ODF / HTML / …
                                   │
NDT + recursos ────────────────────┘

NDF-core + envelope + NDT + schemas + recursos ──► .ndfpkg
```

### 1.1 Dever do formato e responsabilidade do produtor

O formato deve permitir que **toda a informação relevante e necessária possa ser
guardada e reproduzida**. É esse o seu dever, e é só esse.

| | Dever de quem |
|---|---|
| Capacidade de representação — existir lugar para tudo o que é relevante e necessário | **do formato** |
| Correção do que se representa — que o declarado seja verdadeiro, competente, completo e legal | **do produtor** |

O NDF não substitui a responsabilidade dos sistemas produtores e guarda o
documento tal como o produtor o emitiu. Um produtor pode emitir um documento
juridicamente incompleto e o NDF ser válido: o ato existe, e a sua validade é
decidida pelas autoridades administrativas e judiciais competentes, como
sucede com um documento em papel.

O critério que separa os dois deveres é operacional: **um verificador consegue
decidir isto tendo apenas o pacote em mãos?** Se sim, pode ser conformidade. Se
exige o mundo — a lei, a orgânica, o procedimento, os factos — é do produtor.
Ver [ADR-022](ADR-022-dever-do-formato.md).

Decorre daqui que um `.ndfpkg` válido garante integridade, identidade e
interpretabilidade — não legalidade, completude nem correção.

## 2. Responsabilidades

### 2.1 NDF

O NDF representa uma instância documental finalizada. Contém os dados,
metadados e conteúdo lógico que permitem compreender o documento, bem como os
elementos necessários para verificar a sua integridade e, quando aplicável, a
sua autenticidade.

O formato NDF, no sentido de conformidade (specs/ndf/SPEC.md §9.1–§9.3),
divide-se em:

- **NDF-core**: JSON canónico e imutável, incluindo dados, metadados, avaliação
  arquivística, conteúdo NCRTF e a referência exata ao NDT;
- **envelope**: hash do NDF-core, código de verificação, assinaturas ou selos
  opcionais, timestamps e material de validação;
- **`.ndfpkg`**: representação portátil e autocontida, contendo NDF-core,
  envelope, NDT, schemas e recursos necessários para interpretar, verificar e
  renderizar o documento.

Adicionalmente, e como perfil operacional **opcional** — o **Perfil de
Ciclo de Vida NORMORDIS** (SPEC.md §2.4, §9.5) — um sistema custodiante
PODE manter um **registo de custódia**: eventos append-only relativos a
ingestão, acesso, transições de estado, re-selagem e eliminação. Não é
requisito de conformidade NDF; um sistema pode adotar o seu próprio modelo
de gestão de ciclo de vida sem deixar de ser um produtor ou leitor NDF
conforme.

### 2.2 NDT

O NDT é um template declarativo de apresentação. Não contém dados de negócio,
não valida regras do domínio e não calcula valores. Um renderizador verifica
estrutura, versões e referências necessárias à interpretação. Os caminhos são
sempre relativos a `NDF-core.documento`.

Um NDT pode orientar múltiplos formatos de saída. Requisitos específicos de
PDF, ODF ou HTML pertencem a perfis de renderizador, não ao modelo lógico NDT.

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
  a natureza do ato ou a lei aplicável o determinar.

Todo o NDF finalizado DEVE ter NDF-core canonicalizado por JCS e
`payload_hash` SHA-256 (requisito de formato — SPEC.md §9.1). Armazenamento
append-only ou WORM com log de auditoria pertence ao Perfil de Ciclo de
Vida NORMORDIS, opcional (SPEC.md §2.4, §9.5) — reforça a garantia de
imutabilidade de custódia descrita acima, mas não é condição de
conformidade NDF. Um hash sem
uma âncora de custódia permite detectar alterações face a uma cópia conhecida,
mas não impede que um atacante substitua simultaneamente conteúdo e hash.

CAdES NÃO É obrigatório para todos os documentos. Aplicam-se os seguintes
perfis:

| Perfil | Requisito | Uso típico |
|---|---|---|
| `integridade` | JCS + hash (formato) + custódia append-only/WORM + auditoria (Perfil de Ciclo de Vida NORMORDIS, opcional) | registos internos sem ato assinável |
| `selo_institucional` | perfil `integridade` + selo eletrónico CAdES da entidade | prova portátil de origem e integridade institucional |
| `assinatura_avancada` | perfil `integridade` + assinatura CAdES avançada | atos que exigem identificação do signatário |
| `assinatura_qualificada` | perfil `integridade` + assinatura CAdES qualificada | atos para os quais a lei ou política exige assinatura qualificada |

A componente "custódia append-only/WORM + auditoria" destes perfis é o
Perfil de Ciclo de Vida NORMORDIS (SPEC.md §2.4, §9.5) — reforça a garantia
de imutabilidade, mas um sistema pode implementar JCS + hash e adotar o seu
próprio modelo de custódia sem deixar de ser um produtor ou leitor NDF
conforme.

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

## 4. Eficiência, autocontenção e interoperabilidade

Existem duas representações conformes:

- **perfil de custódia**: armazenamento em base de dados do NDF-core canónico e
  envelope; NDTs, schemas, certificados e recursos podem ser deduplicados por
  hash dentro do domínio de custódia, desde que a resolução seja transacional,
  imutável e auditável;
- **perfil portátil**: `.ndfpkg` sem dependências externas, no qual todos os
  objetos referenciados são materializados e inventariados por hash.

Ambos os perfis representam o mesmo documento lógico. O perfil de custódia
otimiza persistência, indexação e deduplicação; o perfil portátil otimiza
transferência, verificação e preservação independente. Um sistema conforme
DEVE poder exportar o primeiro para o segundo sem perda semântica.

A deduplicação é uma otimização física e nunca altera o modelo lógico. Uma
exportação portátil DEVE reconstituir todos os objetos necessários.

## 5. Regras de integração

1. `NDF-core.ndt_version_ref` DEVE corresponder a `NDT.schema_id` e
   `NDT.versao_ndt`.
2. O `.ndfpkg` DEVE incluir esse NDT exato e o respetivo hash no manifesto.
3. `metadados.tipo_documento_ref` DEVE resolver para o schema usado para validar
   `NDF-core.documento`.
4. Um caminho NDT `a.b.c` resolve para `NDF-core.documento.a.b.c`.
5. Um valor NCRTF no NDF-core DEVE validar contra a versão NCRTF declarada e
   cumprir as regras de canonicalização dessa versão.
6. Recursos NDT e NCRTF DEVEM resolver dentro do pacote ou do domínio de
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
