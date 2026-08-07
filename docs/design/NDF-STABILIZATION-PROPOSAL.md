# Proposta de estabilização NDF — Fase 1

**Estado:** proposta arquitetural, não normativa. Nenhuma alteração foi
aplicada a schemas, SPEC.md ou suites nesta fase.
**Depende de:** [`NDF-STABILIZATION-MISSION.md`](NDF-STABILIZATION-MISSION.md),
[`../reports/CURRENT-STATE-ASSESSMENT.md`](../reports/CURRENT-STATE-ASSESSMENT.md) (Fase 0).
**Decisão já tomada pelo utilizador:** PR-001 (revisão pública) trata este
trabalho como parte da própria preparação da revisão — não como um trilho
paralelo nem como algo que aguarda o fecho de uma revisão já aberta. Isto
condiciona a estratégia de versionamento adotada abaixo (§7).

---

## 1. Estratégia de versionamento — decisão de enquadramento

**Proposta:** manter `ndf_version: "1.0.0"` e tratar todas as alterações
desta ronda como **refinamento do draft antes da abertura formal de PR-001**,
registadas em `CHANGELOG.md` sob "[Não publicado]" (secção já existente e já
usada para as últimas rondas de harmonização). Não criar `ndf-core.schema.json`
1.1.0 em paralelo.

**Porquê é seguro:** `GOVERNANCE.md` só impõe imutabilidade de artefactos a
partir do estado **Estável**; NDF 1.0.0 está em **Draft — Revisão pública**,
ainda sem revisão aberta e sem implementação independente conhecida
(`READINESS.md`, gate 6). Não há consumidores externos a proteger. Todas as
adições propostas abaixo são campos **opcionais** (não entram em `required`),
pelo que um documento produzido hoje continua válido depois da alteração.

**Efeito colateral aceite:** a reestruturação do modelo de assinaturas (§4)
move `timestamps`/`validation_material` de nível global do envelope para
nível de cada assinatura. Isto invalida a forma *atual* desses dois campos
(hoje globais) caso já existissem exemplares publicados nesse formato — não
existem (confirmado na Fase 0). Fica marcado como `DECISION REQUIRED` no §4
por ser a única alteração desta ronda que seria uma quebra real se houvesse
adoção externa.

**Alternativa rejeitada:** publicar 1.0.0 tal como está para PR-001 e propor
tudo isto como candidata a 1.1.0. Rejeitada porque a tua decisão desta
conversa foi tratar este trabalho como preparação da própria revisão, não
como sequela dela.

---

## 2. Modelo de relações documentais (`relacoes[]`)

### 2.1 Localização e forma

Novo campo opcional em `ndf-core.schema.json`, ao lado de `documento` e
`avaliacao` — **não** no envelope, para ficar coberto pela assinatura.

```json
"relacoes": {
  "type": "array",
  "minItems": 1,
  "items": { "$ref": "#/$defs/relacao" }
}
```

```json
"$defs": {
  "relacao": {
    "type": "object",
    "required": ["tipo", "alvo"],
    "additionalProperties": false,
    "properties": {
      "tipo": {
        "type": "string",
        "enum": [
          "substitui", "corrige", "complementa", "anula", "responde_a",
          "emite_parecer_sobre", "decide_sobre", "executa", "anexa",
          "deriva_de", "referencia"
        ]
      },
      "alvo": {
        "type": "object",
        "required": ["ndf_id", "payload_hash"],
        "additionalProperties": false,
        "properties": {
          "ndf_id": { "type": "string", "pattern": "<uuid-v4>" },
          "payload_hash": { "type": "string", "pattern": "<ver §6>" },
          "descricao": { "type": "string" }
        }
      },
      "papel": { "type": "string", "minLength": 1 }
    }
  }
}
```

`descricao` cobre o mesmo papel de legibilidade humana que hoje existe em
`despacho.sobre[].descricao`. `papel` é texto livre curto e informativo
(ex.: `"informacao_base"`), não um segundo eixo de classificação — evitar dar-lhe
um enum fechado nesta ronda.

### 2.2 Enum fechado de `tipo` — alternativa considerada e rejeitada

Considerei deixar `tipo` como string livre (`minLength` apenas), para não
bloquear extensões futuras sem nova versão de spec. **Rejeitado**: o resto da
especificação usa sistematicamente enums fechados para vocabulário
controlado (`classificacao_seguranca`, `destino_final`, `forma_contagem`,
`nivel_assinatura`) e resolve extensibilidade por nova versão minor — manter
o mesmo padrão em vez de introduzir uma exceção.

### 2.3 Mapeamento PROV-O (informativo, não normativo no schema)

| `tipo` NDF | Primitiva PROV-O mais próxima |
|---|---|
| `substitui` | `prov:wasRevisionOf` |
| `deriva_de` | `prov:wasDerivedFrom` |
| `emite_parecer_sobre` | `prov:wasInformedBy` |
| `decide_sobre` | `prov:wasInformedBy` |
| `corrige` | `prov:wasRevisionOf` (variante) |
| `complementa`, `anexa`, `referencia` | `prov:wasDerivedFrom` (variante genérica) |
| `anula` | sem equivalente direto — documentar como extensão NORMORDIS |
| `responde_a`, `executa` | sem equivalente direto — documentar como extensão NORMORDIS |

Vai para uma tabela informativa em `docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`,
não para o schema (o schema não deve referenciar vocabulário externo como
requisito de validação).

### 2.4 Reconciliação com `despacho.sobre[]`

**Proposta:** manter `despacho.sobre[]` no registo tal como está (é
`documento`, não é envelope — já está coberto pela assinatura, o problema
nunca foi a assinatura, foi a ausência de hash e a não-reutilização), mas:

1. Acrescentar `payload_hash` opcional a `despacho.sobre[]` numa nova versão
   de registo (`despacho@1.1.0` — versão do **registo**, independente de
   `ndf_version`, conforme `VERSIONING.md` §"Versões do registo").
2. Documentar em `SPEC.md` que `relacoes[]` é o mecanismo **genérico e
   preferencial**; `sobre[]` fica como campo de conveniência de leitura
   específico do tipo `despacho`, e um produtor conforme **DEVE** manter os
   dois coerentes quando ambos estiverem presentes (mesma lista de `ndf_id`).
3. Não obrigar a remoção de `sobre[]` — seria alteração incompatível do
   registo sem benefício correspondente.

**Alternativa considerada:** descontinuar `sobre[]` e forçar todos os tipos a
usar apenas `relacoes[]`. Rejeitada nesta ronda — `sobre[]` já está em
produção conceptual no registo e a migração pode ser feita depois, com dados
reais a informar se vale a pena.

### 2.5 Reconciliação com `versao_anterior`/`hash_anterior` (envelope)

**Proposta:** não remover nem mover. Acrescentar à SPEC.md uma recomendação
(RECOMENDADO, não DEVE) para que um NDF que substitui outro inclua também
`relacoes: [{"tipo": "substitui", "alvo": {"ndf_id": versao_anterior,
"payload_hash": hash_anterior}}]` no core. Isto torna a relação de
substituição **verificável e assinada**, sem quebrar o mecanismo existente
nem excluir documentos que não precisem do modelo geral de relações (ex.:
sistemas que só fazem versionamento linear simples).

**Risco aceite:** duplicação de informação (mesma relação em dois sítios).
Mitigação: `tools/validate.py` (Fase 2/3) deve verificar consistência entre
os dois quando ambos presentes.

---

## 3. Tipo de documento `parecer`

### 3.1 Achado da Fase 0 a resolver primeiro

`informacao-tecnica.schema.json` já descreve o seu propósito como "análise,
**parecer** ou proposta de decisão" — há sobreposição conceptual com o novo
tipo proposto. Decisão: criar `parecer` como tipo **distinto**, porque na
prática administrativa portuguesa um parecer tem estrutura própria (sentido
favorável/desfavorável, fundamentação jurídica, entidade emissora com
competência específica) que `informacao-tecnica` não modela e não deveria
ser forçada a modelar via campos opcionais genéricos. `informacao-tecnica`
mantém-se para notas internas sem essa estrutura formal.

### 3.2 Forma proposta (`specs/registry/schemas/parecer.schema.json`, `parecer@1.0.0`)

Modelado com o mesmo estilo de `informacao-tecnica.schema.json` (consistência
de convenções já estabelecidas no registo):

```json
{
  "required": ["numero", "data", "autor", "sentido", "corpo"],
  "properties": {
    "numero": "string",
    "data": "string (date)",
    "autor": { "nome, cargo, unidade_organica — igual a informacao-tecnica.autor" },
    "sentido": { "enum": ["favoravel", "desfavoravel", "favoravel_condicionado"] },
    "corpo": "string — fundamentação (NCRTF, ver nota)",
    "conclusao": "string, opcional",
    "fundamentacao_juridica": "array de string, opcional — diplomas/normas invocados"
  }
}
```

**Nota a resolver em Fase 2, não aqui:** `informacao-tecnica.corpo` é
`string` simples, não NCRTF, apesar de o exemplo de `oficio` no SPEC.md §2.9.3
usar NCRTF para `documento.corpo`. Isto é uma inconsistência **pré-existente**
entre tipos do registo (fora do âmbito desta missão, mas registo-a para não
ser confundida com algo introduzido agora). `parecer.corpo` seguirá o que
`informacao-tecnica.corpo` já faz (string simples) para não introduzir uma
terceira convenção — a harmonização NCRTF-vs-string-simples nos tipos do
registo fica como item de dívida técnica separado.

O NDF de exemplo do parecer usa `relacoes: [{"tipo": "emite_parecer_sobre",
"alvo": {"ndf_id": <informação>, "payload_hash": <hash>}}]`.

---

## 4. Modelo de assinatura autocontida

### 4.1 Alteração a `envelope.schema.json` `$defs.assinatura`

Adicionar a cada entrada de `assinaturas[]`:

```json
"assinatura_id": { "type": "string", "pattern": "<uuid-v4>" },
"papel": {
  "type": "string",
  "enum": ["autor","coautor","validador","aprovador","decisor",
           "representante","testemunha","selante"]
},
"ordem": { "type": "integer", "minimum": 1 },
"timestamps": { "$ref": "#/$defs/timestamps" },
"validation_material": { "$ref": "#/$defs/validation_material" }
```

`assinatura_id` passa a **required** por entrada (simplifica referenciação
futura — ex.: eventos de custódia que queiram apontar para "qual assinatura
foi renovada"). `papel` e `ordem` ficam opcionais — nem todo o produtor
precisa de os popular, e forçar um valor de `papel` para `selo_institucional`
não faz sempre sentido semântico.

Remover `timestamps` e `validation_material` do nível de topo do envelope,
passando a existir apenas dentro de cada `assinatura`. `$defs.timestamps` e
`$defs.validation_material` tornam-se definições reutilizáveis (extraídas do
que já existe hoje a nível de topo, sem alterar a sua forma interna).

### 4.2 Porque não um modelo dual (global + por assinatura)

Considerei manter os campos globais como "modo de compatibilidade" quando só
há uma assinatura, e usar os novos campos por assinatura só quando há mais
do que uma. **Rejeitado**: cria dois caminhos de leitura válidos para o
mesmo dado, cada verificador tem de saber qual usar, e o ganho de
compatibilidade é nulo (§1 — não há adoção externa a proteger ainda).

### 4.3 `DECISION REQUIRED`

Esta é a alteração de maior risco estrutural desta ronda, por reformular a
forma de um campo já existente (não é só adição). Antes de aplicar em Fase 2:
confirmar que nenhum sistema fora deste repositório já gera envelopes NDF
1.0.0 com `timestamps`/`validation_material` a nível de topo. Assumo que não
(gate "implementação independente" ainda pendente em `READINESS.md`), mas é
uma confirmação tua, não uma inferência minha.

---

## 5. Bloco `participantes`

### 5.1 Forma proposta

Novo campo opcional em `ndf-core.schema.json`:

```json
"participantes": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["participante_ref", "papel"],
    "additionalProperties": false,
    "properties": {
      "participante_ref": { "type": "string", "minLength": 1 },
      "tipo": { "type": "string", "enum": ["pessoa", "sistema", "entidade"] },
      "papel": {
        "type": "string",
        "enum": ["autor","coautor","revisor_humano","validador","aprovador",
                 "decisor","representante","entidade_produtora","sistema_tecnico"]
      }
    }
  }
}
```

### 5.2 Convivência com `informacao-tecnica.autor` e `despacho.decisor`

**Proposta:** manter os campos existentes do registo tal como estão —
descrevem uma pessoa com `nome`/`cargo` para exibição no documento renderizado
(vão para o NDT, aparecem no PDF). `participantes[]` no core é um índice
estrutural paralelo, pensado para consulta/auditoria/grafo, não para
substituir o texto que aparece no documento. **Risco aceite:** redundância
entre os dois quando ambos preenchidos para a mesma pessoa. Não resolvido
nesta ronda — juntar os dois modelos exigiria alterar todos os schemas do
registo, fora do âmbito proporcional desta missão. Fica registado como dívida
técnica para uma versão futura, não como decisão de fundir agora.

---

## 6. Padrão de hash agnóstico de algoritmo

**Proposta:** substituir `^sha256:[0-9a-f]{64}$` por
`^[a-z][a-z0-9-]*:[0-9a-f]+$` em: `envelope.schema.json` (`payload_hash`,
`hash_anterior`), `manifest.schema.json` (`payload_hash`), `custody-event.schema.json`
(`previous_event_hash`, `event_hash`), e usar o mesmo padrão em
`relacoes[].alvo.payload_hash` (§2.1).

`payload_hash_alg` continua fixo a `["sha256"]` nesta versão (SPEC.md §2.5 já
compromete a mudança para 1.2.0 — não antecipar isso aqui). O padrão de
string generalizado é **estritamente mais permissivo** que o atual — qualquer
valor hoje válido (`sha256:` + 64 hex) continua a validar. Não há
incompatibilidade a discutir.

**Não incluído nesta ronda:** o algoritmo de derivação do `validation_code`
(§4.6.2 SPEC.md) está hardcoded a SHA-256 no próprio algoritmo, não só no
formato da string — mudar isso é uma alteração de comportamento observável,
não de padrão de validação, e fica fora do âmbito desta proposta.

---

## 7. Bloco `proveniencia_ia`

### 7.1 Forma proposta

```json
"proveniencia_ia": {
  "type": "object",
  "required": ["utilizada"],
  "additionalProperties": false,
  "properties": {
    "utilizada": { "type": "boolean" },
    "intervencoes": {
      "type": "array",
      "items": { "$ref": "#/$defs/intervencao_ia" }
    }
  },
  "if": { "properties": { "utilizada": { "const": false } } },
  "then": { "properties": { "intervencoes": { "maxItems": 0 } } },
  "else": { "required": ["intervencoes"], "properties": { "intervencoes": { "minItems": 1 } } }
}
```

```json
"$defs": {
  "intervencao_ia": {
    "type": "object",
    "required": ["intervencao_id", "finalidade", "sistema", "executada_em",
                 "resultado_incorporado", "revisao_humana"],
    "additionalProperties": false,
    "properties": {
      "intervencao_id": { "type": "string", "pattern": "<uuid-v4>" },
      "finalidade": {
        "type": "string",
        "enum": ["apoio_redacao","resumo","classificacao","pesquisa",
                 "traducao","deteccao_erros","outro"]
      },
      "finalidade_detalhe": { "type": "string" },
      "sistema": {
        "type": "object",
        "required": ["nome", "fornecedor"],
        "properties": {
          "nome": { "type": "string" },
          "fornecedor": { "type": "string" },
          "modelo": { "type": "string" },
          "versao": { "type": "string" }
        },
        "additionalProperties": false
      },
      "executada_em": { "type": "string", "format": "date-time" },
      "resultado_incorporado": {
        "type": "string",
        "enum": ["integralmente", "parcialmente", "nao_incorporado"]
      },
      "segmentos_afetados": { "type": "array", "items": { "type": "string" } },
      "revisao_humana": {
        "type": "object",
        "required": ["estado"],
        "properties": {
          "estado": {
            "type": "string",
            "enum": ["pendente","revisto_e_aprovado","revisto_com_alteracoes","rejeitado"]
          },
          "revisor_ref": { "type": "string" },
          "revisto_em": { "type": "string", "format": "date-time" }
        },
        "if": { "properties": { "estado": { "enum": ["revisto_e_aprovado","revisto_com_alteracoes","rejeitado"] } } },
        "then": { "required": ["revisor_ref", "revisto_em"] },
        "additionalProperties": false
      },
      "evidencia_ref": {
        "type": "object",
        "properties": {
          "tipo": { "type": "string" },
          "identificador": { "type": "string" },
          "hash": { "type": "string", "pattern": "<ver §6>" }
        },
        "additionalProperties": false
      }
    }
  }
}
```

`finalidade_detalhe` segue o mesmo padrão já usado em `forma_contagem`/
`forma_contagem_detalhe` (SPEC.md §3.3) — reutilização de convenção
existente, não invenção de uma nova.

### 7.2 Porque `revisao_humana` é obrigatório por intervenção, não opcional

Alternativa considerada: tornar `revisao_humana` opcional, só presente
quando aplicável. **Rejeitado** — se o princípio "Human in the Loop" (§7 do
brainstorming original) é para ter algum peso técnico, a ausência de revisão
tem de ser **representável e visível** (`estado: "pendente"`), não omissível
por omissão do campo. Omitir o campo apagaria a distinção entre "ainda não
revisto" e "não se aplica revisão", que são coisas diferentes.

### 7.3 Documento informativo companheiro

Criar `docs/normalization/AI-PROVENANCE-GUIDANCE.md` (Fase 2), com a
formulação de não-conformidade automática já acordada (ver missão §8) e
exemplos de preenchimento mínimo vs. completo.

---

## 8. Nota sobre custódia (achado adicional da Fase 1, fora do pedido original)

Ao desenhar a reconciliação de `relacoes[]` com transições de `estado`,
notei duas lacunas pequenas, de baixo risco, que ficam melhor resolvidas
agora do que depois:

1. **Transição de estado causada por relação externa** (ex.: `estado`
   transita para `"substituido"` porque outro NDF criou uma relação
   `substitui` apontando para este). O `custody-event.schema.json` já tem um
   campo `details` livre (`type: "object"`, sem schema fechado) — proposta:
   usar esse campo existente para registar
   `{"causado_por_relacao": {"ndf_id": "...", "tipo": "substitui"}}`, sem
   alterar o schema de custódia. Reutilização, não adição.
2. **Tombstone de eliminação (SPEC.md §2.4.3) não tem schema próprio.** É
   descrito em prosa, mas nenhum ficheiro `.schema.json` o valida. Proposta:
   representá-lo como `custody-event` com `event_type: "eliminado"` e os
   campos do tombstone dentro de `details` — de novo, reutilização do
   mecanismo já existente em vez de um novo ficheiro de schema. Alternativa
   (novo `tombstone.schema.json` dedicado) fica anotada mas não recomendada,
   por aumentar a superfície de schemas sem necessidade demonstrada.

---

## 9. Impacto em suites e exemplos (visão geral — detalhe fica para Fase 2)

- `conformance/ndf/valid/`: nenhum dos 6 casos existentes deixa de validar
  (todos os campos novos são opcionais). Adicionar novos casos para
  `relacoes`, assinatura múltipla e `proveniencia_ia`.
- `conformance/ndf/invalid/`: adicionar os casos já enumerados na missão
  (§9) — relação sem hash, revisão humana "concluída" sem revisor/data,
  `utilizada: false` com intervenções presentes, etc.
- `specs/ndf/examples/ndfpkg-example/`: o exemplo `.ndfpkg` atual usa uma
  única assinatura — precisa de decisão em Fase 2 sobre se este exemplo
  histórico se mantém como está (ilustra o caso simples) ou se é acrescentado
  um segundo exemplo com múltiplas assinaturas, mantendo o primeiro intacto.
  Recomendo o segundo (não alterar o exemplo existente).
- Exemplo novo Informação → Parecer → Despacho: três `.ndfpkg` ou três NDF
  soltos — a decidir em Fase 2 consoante o que for mais legível para revisão
  externa.

---

## 10. Riscos

| Risco | Mitigação proposta |
|---|---|
| Reestruturação do envelope (§4) invalida forma anterior de `timestamps`/`validation_material` | `DECISION REQUIRED` §4.3 — confirmar ausência de adoção externa antes de aplicar |
| Redundância `participantes[]` vs. campos do registo (§5.2) | Aceite conscientemente, não resolvida agora; registar como dívida técnica |
| Redundância `relacoes[]` vs. `despacho.sobre[]` (§2.4) | Documentar precedência (`relacoes[]` é a fonte autoritativa) e verificar consistência no validador |
| Enum fechado de `tipo` de relação limita casos futuros não previstos | Extensão só por nova versão minor — consistente com o resto da spec, não é uma limitação nova |
| Sobrecarga de trabalho de Fase 2 (6 áreas em simultâneo) | Sequenciar por dependência: relações → parecer → assinaturas → participantes → IA → hash (ordem já usada nas secções acima) |

---

## 11. Questões `DECISION REQUIRED` (resumo)

1. **§1** — confirmar que manter `ndf_version: "1.0.0"` (em vez de bump) está
   correto dado o enquadramento "preparação da revisão" já confirmado.
2. **§4.3** — confirmar ausência de consumidores externos do formato atual de
   envelope antes de mover `timestamps`/`validation_material` para dentro de
   cada assinatura.

Todas as restantes decisões desta proposta usam defaults conservadores e
ficam sujeitas a objeção antes da Fase 2, mas não bloqueiam o arranque dela.

---

## 12. Próximo passo

Mediante a tua confirmação (ou correção) dos dois pontos do §11, a Fase 2
implementa por esta ordem: (1) `relacoes[]` + reconciliação; (2) `parecer.schema.json`;
(3) assinatura autocontida; (4) `participantes[]`; (5) `proveniencia_ia`;
(6) padrão de hash; (7) exemplo Informação→Parecer→Despacho completo;
(8) ADRs correspondentes; (9) atualização de `conformance/`; (10) rerun de
`tools/build_requirements_index.py` e `tools/audit_normative.py`.
