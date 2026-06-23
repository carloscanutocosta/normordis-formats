# Política de Versões

## Princípios

As especificações seguem versionamento semântico (semver):

- **Major** (`x.0.0`): alterações incompatíveis — campos obrigatórios removidos ou renomeados, semântica alterada. Leitores devem declarar suporte explícito a cada versão major.
- **Minor** (`1.x.0`): adições compatíveis — novos campos opcionais. Leitores existentes continuam a funcionar.
- **Patch** (`1.0.x`): clarificações, correção de erros tipográficos, alterações não normativas. Sem impacto comportamental.

## Estado da especificação

Cada versão publicada assume um dos níveis definidos em
[NORMALIZATION.md](NORMALIZATION.md). Não são mantidas taxonomias de estado
paralelas.

O estado é independente da versão.

Exemplos:

- NDF v1.0.0 — Draft
- NDF v1.0.0 — Revisão pública
- NDF v1.1.0 — Candidata

## Versão da especificação vs. versão do template

`ndf_version` / `ndt_version` rastreia a **versão da especificação de formato** — muda apenas quando o próprio formato muda.

`versao_ndt` (NDT) rastreia a **versão da instância do template** — pode mudar anualmente para formulários fiscais sem alterar a versão da especificação. Exemplo: `modelo3-irs-rosto@2026.1` é o template de 2026 numa especificação NDT 2.0.0 inalterada.

## Garantias de estabilidade

- Caminhos canónicos de campo (`id`s) nunca são renomeados entre versões minor.
- Campos descontinuados são marcados `"descontinuado": true` em vez de removidos, preservando a legibilidade de documentos mais antigos.
- URLs, hashes e artefactos de versões publicadas anteriores permanecem disponíveis.

## Compatibilidade e schemas

Cada schema valida exactamente a versão indicada no seu `$id`; o campo de versão usa `const`, não um padrão SemVer genérico. Um leitor só declara suporte a versões que reconheça explicitamente.

Uma versão minor pode acrescentar campos ou nós opcionais, mas um documento que os use declara a nova versão. Leitores antigos não devem ignorar silenciosamente conteúdo assinado desconhecido. Podem recusar o documento ou operá-lo apenas em modo opaco, sem afirmar interpretação completa.

## Declaração de conformidade

Uma implementação deve declarar explicitamente o âmbito da conformidade que afirma suportar.

Exemplo:

```text
Specification: NDF
Version: 1.0
Role: Producer
Conformance Suite: 1.0.0
```

Sempre que possível, a declaração deve indicar:

- especificação;
- versão;
- papel (produtor, leitor, renderizador ou verificador);
- perfil suportado;
- versão da suite de conformidade utilizada.

## Versões do registo

O registo de tipos de documento (`specs/registo/schemas/`) segue um esquema de versão próprio, independente das versões NDF/NDT/NCRTF:

- Cada tipo canónico tem um identificador estável: `oficio`, `despacho`, `modelo3-irs`, etc.
- A versão de campanha ou de publicação é declarada no `tipo_documento_ref` do NDF-core: `"modelo3-irs@2026"`, `"oficio@1.0.0"`.
- Uma nova campanha fiscal (e.g., `modelo3-irs@2027`) constitui uma versão nova no registo, mas não implica uma versão nova de NDF ou NDT, a não ser que o formato em si mude.
- Schemas do registo com `additionalProperties: true` permitem campos futuros sem quebra de versão; schemas com `additionalProperties: false` exigem uma nova versão do registo para cada adição de campo.

## Artefactos abrangidos

Uma versão publicada inclui como unidade indivisível:

- texto normativo;
- JSON Schemas;
- registo e schemas de tipos canónicos;
- exemplos e vetores canónicos;
- suite e runner de conformidade.

Alterar comportamento observável de qualquer destes artefactos exige uma nova versão. URLs, hashes e artefactos de versões publicadas anteriores permanecem disponíveis.
