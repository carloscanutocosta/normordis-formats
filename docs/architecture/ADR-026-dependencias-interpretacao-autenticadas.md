# ADR-026: `dependencias_interpretacao` — ligação criptográfica a NDT e schemas

**Estado**: Aceite
**Data**: 2026-09-11
**Decisores**: carloscanutocosta

---

## Contexto

Avaliação técnica externa ao commit `a9d72f8577ed6d92021c4b17ac9b0eef4eba9505`
reproduziu o seguinte: copiar o pacote de exemplo, substituir um texto fixo do
NDT por outro, manter `schema_id` e `versao_ndt` inalterados, recalcular
apenas o `hash_sha256` da entrada correspondente em `manifest.inventario` —
e o validador aceita o pacote alterado, com os mesmos bytes de `ndf-core.json`
e `envelope.json`. Registado como `R16` em
[`docs/reports/READINESS-ASSESSMENT.md`](../reports/READINESS-ASSESSMENT.md)
§5.6.

A causa é estrutural, não um bug de verificação em falta. `ndt_version_ref`
(§2.6) é uma **etiqueta** — `"<schema_id>@<versao_ndt>"` — não um hash. Está
dentro dos `payload_bytes` e portanto coberta pela assinatura, mas o que ela
vincula é *que versão* do NDT deve ser usada, não *que bytes* constituem essa
versão. O hash do ficheiro NDT só existe em `manifest.inventario`
(specs/ndt/SPEC.md §1.1), que **não está** coberto pela assinatura sobre o
NDF-core — é inventário físico do pacote, recalculável por qualquer processo
que o gere, incluindo um adversário.

`docs/reports/READINESS-ASSESSMENT.md` §4.2.1 já tinha uma resposta de debate
para uma versão mais fraca desta pergunta — «a assinatura vincula dados e
versão do template» — que ficou corrigida no mesmo achado: versão não é bytes.

O mesmo problema atravessa duas outras dependências de interpretação, pela
mesma razão estrutural: o schema do tipo documental (quando extensão
qualificada, NDF-PROD-018) e o schema do perfil de avaliação (§3.2.3,
sempre obrigatório em `schemas/`) — ambos materializados no `.ndfpkg`, ambos
com integridade garantida apenas pelo `manifest.json`, nunca pelos bytes
assinados.

Os recursos do NDT (fontes, imagens) **não** têm este problema — já estão
resolvidos por desenho: `ndt.schema.json` define `Recurso` como
`RecursoEmbebido` (bytes dentro do próprio NDT) ou
`RecursoReferenciadoPorHash` (`hash_sha256` **dentro do NDT**, e o nome do
ficheiro em `recursos/` é o próprio hash — §8.1). Uma vez que o hash do NDT
esteja vinculado (este ADR), o hash de cada recurso hash-referenciado fica
transitivamente coberto, por estar dentro dos bytes do NDT. O que falta nesse
ponto não é um novo campo — é o verificador confirmar que o ficheiro em
`recursos/<hash>.<ext>` hashes efetivamente para `<hash>` (`tools/validate.py`
não o faz hoje; corrigido na mesma ronda desta ADR, registado como `R23`).

## Decisão

Novo campo **obrigatório** de topo no NDF-core, `dependencias_interpretacao`:
um array de `{ papel, ref, hash_sha256 }`, cada entrada vinculando por hash
uma dependência de interpretação materializada no `.ndfpkg`.

```json
"dependencias_interpretacao": [
  { "papel": "ndt", "ref": "oficio-generico@2.0.0", "hash_sha256": "sha256:…" },
  { "papel": "schema_perfil", "ref": "pt-dglab", "hash_sha256": "sha256:…" }
]
```

| `papel` | Obrigatória quando | `ref` | Ficheiro correspondente |
|---|---|---|---|
| `"ndt"` | Sempre — todo o NDF tem `ndt_version_ref` | igual a `ndt_version_ref` | `ndt/<schema_id>@<versao>.ndt.json` |
| `"schema_tipo"` | `metadados.tipo_documento_ref` usa extensão qualificada (mesma condição de `NDF-PROD-018`) | igual a `tipo_documento_ref` | `schemas/<tipo_id>.schema.json` |
| `"schema_perfil"` | `avaliacao.perfil` está declarado (sempre obrigatório em `schemas/`, §8.1) | igual a `avaliacao.perfil` | `schemas/<perfil>.schema.json` |

`hash_sha256` é o SHA-256 dos **bytes brutos** do ficheiro tal como
materializado no pacote — a mesma convenção já usada em
`manifest.inventario[].hash_sha256` (§8.2) e em
`documento.componentes[].sha256` ([ADR-021](ADR-021-componentes-nos-bytes-assinados.md)).
Não é JCS: NDT e schemas não têm hoje requisito de canonicalização própria, e
impor um adicionaria uma segunda máquina de canonicalização por um ganho que
o hash de bytes brutos já entrega — determinismo suficiente, porque o ficheiro
é gerado uma vez e não reserializado (mesmo princípio de `NDF-PROD-020`).

**Resolução por identificador, nunca por caminho** — `ref` identifica a
dependência, `hash_sha256` verifica-a; o nome do ficheiro dentro de `ndt/` ou
`schemas/` pode ser reorganizado sem invalidar nada, desde que o conteúdo e o
identificador se mantenham. Mesmo princípio de `NDF-PKG-009` para
`componentes[]`.

### O teste de admissão de novas primitivas (`ROADMAP.md`)

1. É informação documental? Não é sobre o ato — é sobre o que rege a sua
   interpretação.
2. Cabe em `documento`, via schema do tipo? Não — atravessa todos os tipos,
   não é específico de nenhum.
3. Cabe num bloco transversal existente? Não — nenhum dos blocos existentes
   (`metadados`, `avaliacao`, `relacoes`, `participantes`,
   `proveniencia_sistema`, `proveniencia_ia`, `imputacao`) descreve
   dependências de interpretação.
4. É variação jurisdicional? Não.
5. **Pode viver fora do NDF, referenciada por hash?** Sim — e este é
   exatamente o padrão já usado para evidência de IA, regras de sistema e
   artefactos externos: referência mais hash, sem inchar o documento com o
   conteúdo. `dependencias_interpretacao` **é** esse padrão aplicado a NDT e
   schemas, não uma primitiva nova por analogia — é a mesma primitiva.

A quinta resposta é afirmativa, o que — pela lógica do próprio teste —
significa que isto não é uma primitiva pesada a admitir por exceção; é o
mecanismo leve já estabelecido, aplicado a uma dependência que ainda não o
usava. Ver também a alternativa "primitiva nova" rejeitada abaixo.

## Alternativas consideradas

### Hash direto em `ndt_version_ref` (transformar em objeto)

Substituir `"ndt_version_ref": "oficio-generico@2.0.0"` por
`{ "ref": "...", "hash_sha256": "..." }`. Resolveria o caso do NDT, mas não os
dos dois schemas, que ficariam sem mecanismo próprio — duas soluções para o
mesmo problema. Rejeitada por não cobrir `R16` por inteiro.

### Manifesto de dependências como ficheiro à parte, com um único hash em NDF-core

Considerada no plano inicial de resposta a `R16`. Adiciona uma indireção — um
novo tipo de ficheiro no pacote, com o seu próprio schema e a sua própria
canonicalização — para um ganho marginal (um hash a menos no NDF-core, à
custa de um ficheiro a mais no `.ndfpkg` e mais uma superfície de
canonicalização). Rejeitada por [ADR-021](ADR-021-componentes-nos-bytes-assinados.md)
já ter resolvido o mesmo tipo de problema (componentes binários) com
declaração inline, sem indireção — manter consistência com esse precedente.

### Hash de todo o `.ndfpkg`

Assinar o ZIP inteiro, não apenas o NDF-core. Rejeitada: quebra a distinção
entre "artefacto NDF assinado" (`NDF-core` + `Envelope`) e "pacote de
distribuição" (§1.2) — o `.ndfpkg` é uma materialização portátil, pode ser
reorganizado (outros nomes de ficheiro, outra compressão) sem deixar de
corresponder ao mesmo documento. Hashear o ZIP tornaria qualquer
reempacotamento uma quebra de integridade, mesmo sem alteração de conteúdo.

### Exigir apenas para `nivel_assinatura ∈ {"avancada", "qualificada"}`

Rejeitada: `validation_code` e a verificação de integridade de
`payload_bytes` aplicam-se também a `nivel_assinatura: "nenhuma"` (§2.10.4).
Tornar `dependencias_interpretacao` condicional ao nível de assinatura
deixaria exactamente os documentos sem assinatura pessoal — que dependem
inteiramente da integridade do hash para qualquer garantia — sem a proteção
que mais precisam dela.

## Justificação da decisão

Aplica-se aqui o mesmo raciocínio de ADR-021, com o mesmo alvo: **se o hash
vive só no manifesto, substituir o ficheiro e regerar o manifesto produz um
pacote que passa toda a validação existente** — a assinatura continua válida,
porque assina outra coisa. Declarado em NDF-core, o hash entra em
`payload_bytes`, é canonicalizado por JCS e fica coberto pela assinatura e
pelo timestamp de arquivo, tal como qualquer outro campo do NDF-core.

A junta verificável nova é a coerência entre `dependencias_interpretacao[]` e
os ficheiros materializados em `ndt/` e `schemas/` — mesma estrutura de
`NDF-PKG-009`, aplicada a uma classe de ficheiro diferente.

## Consequências

**Positivas**: o ataque reproduzido na avaliação externa deixa de passar —
alterar o NDT e recalcular apenas `manifest.json` deixa de bastar, porque
`ndf-core.json` (dentro dos bytes assinados) passa a conter o hash correto, e
o divergiria do ficheiro alterado. Fecha `R16`. O mesmo mecanismo cobre, sem
campo adicional, os dois schemas materializados no pacote.

**Negativas / mitigações**: **campo novo obrigatório** — alteração
incompatível ao NDF-core, ao abrigo do mesmo raciocínio das reaberturas de D5
de 2026-08-13 e 2026-08-20 (`ROADMAP.md`): nível 1 — Draft, sem revisão
pública aberta, sem utilizadores externos, custo de alteração hoje é o mais
baixo que alguma vez será. Terceira reabertura pontual de D5, registada como
tal em `ROADMAP.md`. `ndf_version` mantém-se em `1.0.0` (ADR-007) — não há
instâncias externas a migrar.

O produtor tem agora de calcular três hashes adicionais (no máximo) por
documento finalizado — custo baixo, mecânico, mesma família de operação que
já faz para `payload_hash`.

`dependencias_interpretacao` duplica, em hash, informação que já existe em
`manifest.inventario` para os mesmos ficheiros. Não é duplicação de
responsabilidade — uma é documental e assinada, a outra é física do pacote —
mas exige coerência entre as duas (`NDF-PKG-010`, novo, mesmo padrão de
`NDF-PKG-009`).

## Referências

- SPEC.md §1.2 (composição), §2.6 (`ndt_version_ref`), §2.6.2 (novo,
  `dependencias_interpretacao`), §8.1 (composição do `.ndfpkg`), §9.1
  (`NDF-PROD-024`, `NDF-PROD-025`), §9.2 (`NDF-READ-025`), §9.3
  (`NDF-PKG-010`)
- `specs/ndt/SPEC.md` §1.1 — corrigido nesta ronda
- [ADR-021](ADR-021-componentes-nos-bytes-assinados.md) — precedente direto:
  mesmo raciocínio aplicado a componentes binários
- [ADR-007](ADR-007-versionamento-estabilizacao.md) — custo de alteração
  incompatível antes de publicação
- `docs/reports/READINESS-ASSESSMENT.md` §4.2.1 (corrigida), §5.6 (`R16`,
  `R23`)
- `ROADMAP.md` — Fase 1E, P0.2, terceira reabertura pontual de D5
