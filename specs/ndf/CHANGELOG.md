# Histórico NDF

## Não publicado

### Acrescentado

- **§2.8.1 — componentes binários referenciados por hash.** A proibição de §2.8
  passa a recair sobre bytes embutidos, não sobre a referência a eles: um schema
  de tipo documental PODE declarar componentes por digest, mantendo os bytes fora
  do NDF-core. Decisão de âmbito registada em `ROADMAP.md` (2026-08-20); o
  NDF-core não é alterado e `ndf_version` mantém-se em `1.0.0`. Ver ADR-020 e
  ADR-021.
- **§2.8.2 — divergência entre declaração e componente.** O componente é
  autoritativo quanto ao conteúdo do ato; o NDF quanto a identidade, custódia e
  classificação. Nenhum corrige o outro.
- **§4.5.1 — assinaturas contidas em componentes.** `nivel_assinatura` não se
  deriva delas; os bytes assinados nunca se reescrevem; o material de validação
  congela-se na captura; a ordem assinar → hash do assinado → declarar →
  finalizar é normativa.
- **§8.1** — diretórios `original/`, `representacoes/`, `anexos/` e
  `evidencias/` na composição do `.ndfpkg`. A correspondência com a declaração
  faz-se pelo digest e nunca pelo caminho.
- **`NDF-PROD-020`, `NDF-PROD-021`, `NDF-PROD-022`** — não reescrever
  componentes; não declarar localização de armazenamento; não derivar
  `nivel_assinatura` de assinatura contida.
- **`NDF-READ-021`, `NDF-READ-022`, `NDF-READ-023`** — não apresentar a projeção
  do NDT de um capturado como sendo o documento; não apresentar assinatura de
  componente como assinatura do NDF; resolver componentes por digest.
- **`NDF-PKG-009`** — coerência entre `documento.componentes[].sha256` e
  `manifest.inventario`. É a única junta verificável nova.

### Notas

`manifest.schema.json` não é alterado: o inventário do pacote já cobre a
integridade física de qualquer ficheiro, e a declaração documental vive em
`documento`. Os vetores negativos de `NDF-PKG-009` entram com o exemplo de
captura (`docs/roadmap/PLANO-CAPTURA-NDFPKG.md`, Fase D).


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
