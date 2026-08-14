# Histórico NDF

## [Não publicado] — avaliação arquivística por perfil e separação custódia ↔ RGPD

`ndf_version` mantido em `1.0.0` (ADR-007) — alterações **incompatíveis**
absorvidas antes de qualquer publicação. Ver `CHANGELOG.md` na raiz para o
detalhe completo.

- adicionado: `avaliacao.perfil`, com schemas de perfil em
  `specs/registry/profiles/` e obrigação de viajarem no `.ndfpkg`
  (NDF-PKG-008); perfis `pt-dglab` e `generic` (ADR-015);
- adicionado: `destino_final: "a_determinar"` com `autoridade_avaliacao`, para
  sistemas em que a decisão de destino não compete ao produtor;
- alterado: `tipo_classificacao_ref` → `classificacao_ref`;
  `instrumento_avaliacao_versao_ref` → `instrumento_ref`;
  `prazo_conservacao_administrativa` → `prazo_conservacao`;
- adicionado: `metadados.entidade_responsavel` (custódia do registo);
- alterado: campos RGPD agrupados em `metadados.protecao_dados`, obrigatório
  se e só se `contem_dados_pessoais: true` (ADR-016).

## [Não publicado] — proveniência de sistema e imputação jurídica

`ndf_version` mantido em `1.0.0` (ADR-007). Ver `CHANGELOG.md` na raiz para o
detalhe completo.

- adicionado: `proveniencia_sistema` (array) — sistema determinístico que
  produziu o conteúdo, com ordem cronológica normativa (ADR-013);
- adicionado: `imputacao` (array) — quem responde juridicamente e a que
  título, com bloco opcional `autenticacao` por entrada (ADR-012);
- adicionado: invariante de origem — todo o NDF declara origem humana, de
  sistema ou de IA (§2.2.1);
- alterado: `participantes` passa a índice exclusivamente de pessoas
  singulares; removidos `tipo`, `sistema_tecnico`, `entidade_produtora`,
  `validador` e `aprovador`; acrescentados `responsavel_tecnico` e
  `qualificacao`;
- adicionado: `tipo_documento_ref` aceita `ext.<entidade>.<tipo>@<versao>`,
  com o schema a viajar no pacote (ADR-014).

## [1.0.0] — Draft — Revisão pública

- Especificação inicial: estrutura NDF-core, envelope CAdES-B-LTA, avaliação
  arquivística, pipeline de finalização, proveniência e versionamento.
