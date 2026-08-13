# Histórico NDF

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
