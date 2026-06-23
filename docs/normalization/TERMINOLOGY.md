# Base terminológica NORMORDIS

A coluna portuguesa contém os termos preferidos no texto normativo. A coluna
inglesa destina-se a traduções controladas; não cria uma segunda versão
normativa. Em caso de divergência, prevalece a definição portuguesa publicada
na especificação aplicável.

| Português preferido | Inglês controlado | Nota de utilização |
|---|---|---|
| especificação | specification | evitar “spec” em prosa normativa |
| schema JSON | JSON Schema | manter o nome da tecnologia; evitar “esquema” quando possa criar ambiguidade |
| registo | registry | catálogo versionado de identificadores e schemas |
| renderizador | renderer | implementação que combina NDF e NDT |
| produtor | producer | implementação que cria uma instância conforme |
| leitor | reader | implementação que interpreta uma instância |
| verificador | verifier | implementação que avalia integridade e conformidade |
| conteúdo canónico | canonical content | conteúdo com representação determinística |
| canonicalização | canonicalization | transformação para representação canónica |
| autocontido | self-contained | sem dependências externas para o perfil declarado |
| perfil de custódia | custody profile | representação otimizada para persistência e deduplicação |
| perfil portátil | portable profile | `.ndfpkg` autocontido |
| interoperabilidade | interoperability | interpretação equivalente por implementações independentes |
| conformidade | conformance | satisfação de requisitos desta especificação |
| declaração de conformidade | conformance claim | declaração de terceiro, não certificação do projeto |
| versão publicada | release | conjunto imutável de artefactos versionados |
| revisão pública | public review | período formal de comentários e resolução documentada |
| requisito | requirement | obrigação expressa por **DEVE** ou **NÃO DEVE** |
| recomendação | recommendation | orientação expressa por **RECOMENDA-SE** |
| permissão | permission | possibilidade expressa por **PODE** |

Termos específicos de NDF, NDT e NCRTF permanecem definidos nas respetivas
cláusulas “Termos e definições”.
