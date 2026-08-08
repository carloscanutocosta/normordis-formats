# Revisão adversarial pré-RC — NDF 1.0

**Estado:** ✅ **todos os 16 achados resolvidos** (2026-08-08). Este
documento passa a ser o registo histórico da revisão; o estado de cada
achado está na tabela de resolução no fim. As decisões de fundo foram
tomadas pelo responsável do projeto e estão registadas em ADR-011 e no
`CHANGELOG.md`.
**Data:** 2026-08-08
**Base:** commit `91076ce`
**Método:** ao contrário das revisões anteriores (que perguntavam *o que
falta ao NDF?*), esta procura **contradições, redundâncias, ambiguidades e
requisitos impossíveis de implementar** — o que não devia lá estar, ou o
que está descrito de forma que dois implementadores conformes
interpretariam de maneira diferente.

## Âmbito verificado

| Eixo | Método | Resultado |
|---|---|---|
| Referências `§X.Y` resolvem | script sobre 4 SPECs | ✅ 90 referências, 0 quebradas (5 sinalizadas eram cruzadas entre documentos, todas válidas) |
| Blocos JSON normativos validam contra o próprio schema | script: 14 blocos extraídos da SPEC NDF | ❌ 3 falham |
| Campos de schema documentados na SPEC | script bidirecional | ❌ 12 campos sem documentação |
| Casos de conformidade documentados no README | comparação ficheiros↔README | ❌ 14 de 28 ausentes |
| Resíduos da ADR-004 (assinatura autocontida) | leitura dirigida | ❌ 2 cláusulas por atualizar |
| Redundâncias core↔envelope | leitura dirigida | ⚠️ 2 confirmadas |

**Não verificado nesta ronda**: leitura manual integral de `specs/ndt/SPEC.md`
e `specs/ncrtf/SPEC.md` (só os cruzamentos automáticos); perfis de
renderizador; contrato OpenAPI do portal.

---

## Bloqueadores — seguir a SPEC à letra produz artefactos inválidos

### F1. §2.4.2 — o exemplo normativo do log de custódia falha o schema que a própria cláusula torna obrigatório

§2.4.2 afirma: *"Cada entrada DEVE validar contra `custody-event.schema.json`"*
— e a seguir apresenta, sob o título **"Estrutura mínima de cada entrada do
log de auditoria"**, um objeto com tabela de campos obrigatórios.

Validado mecanicamente contra o schema: **9 erros**.

| | Campos |
|---|---|
| Exigidos pelo schema | `custody_event_version`, `event_id`, `ndf_id`, `sequence`, `event_type`, `occurred_at`, `actor`, `previous_event_hash`, `event_hash` |
| Presentes no exemplo da SPEC | `ndf_id`, `estado_anterior`, `estado_novo`, `timestamp`, `motivo`, `actualizador`, `instrumento_legal` |
| Interseção | **apenas `ndf_id`** |

Os 6 campos que a SPEC declara obrigatórios (`estado_anterior`, `estado_novo`,
`timestamp`, `motivo`, `actualizador`, `instrumento_legal`) são **proibidos**
pelo schema (`additionalProperties: false`). Os 8 restantes exigidos pelo
schema não aparecem na SPEC.

São dois modelos de dados diferentes a coexistir sob o mesmo nome. Um
implementador que siga a tabela da SPEC produz eventos que o
`tools/check_custody.py` rejeita.

**Decisão necessária:** qual dos dois é o modelo pretendido? O schema parece
ser o mais recente (tem cadeia de hash, `sequence`, ancoragem — que a prosa
de §2.4.2 descreve corretamente no parágrafo anterior); a tabela e o exemplo
parecem ser um estrato anterior nunca removido. Se assim for, a correção é
substituir exemplo+tabela pela estrutura real do schema, mapeando os campos
semânticos antigos (`motivo`, `instrumento_legal`) para `details`.

### F2. §8.2 — o exemplo do `manifest.json` omite 3 campos obrigatórios

O exemplo apresentado como estrutura do manifesto omite `estado`,
`nivel_assinatura` e `validation_code` — os três em `required` no
`manifest.schema.json`. Validação: **8 erros** (3 por omissão, restantes por
usar `"uuid"` e `"sha256:abc123..."` como placeholders literais).

O `.ndfpkg` de exemplo real (`specs/ndf/examples/ndfpkg-example/manifest.json`)
tem os três campos e valida — ou seja, a SPEC está desalinhada tanto do
schema como do exemplo funcional.

### F3. §8.3 e §2.3 — atribuem ao manifesto campos que o schema proíbe

§8.3: *"o `manifest.json` regista `versao_anterior` e `hash_anterior` quando
aplicável, permitindo reconstruir a cadeia de versões com múltiplos
`.ndfpkg`"*. §2.3 repete: *"referência primária em `versao_anterior`, no
manifest do `.ndfpkg`"*.

`manifest.schema.json` tem `additionalProperties: false` e **não declara
nenhum dos dois campos**. A garantia de reconstrução da cadeia de versões
entre pacotes, tal como está escrita, é impossível de implementar de forma
conforme.

**Decisão necessária:** acrescentar os campos ao schema do manifesto, ou
retirar a afirmação da SPEC? Ver F8 e F9 — a resposta depende do destino que
se der ao mecanismo `versao_anterior`.

---

## Alto — contradições entre cláusulas normativas

### F4. §2.10.3 — tabela ainda trata `timestamps`/`validation_material` como campos de topo do envelope

A tabela "Implicações para o envelope" tem colunas `timestamps` e
`validation_material` ao nível do envelope, com valores "Presente/Ausente"
por `nivel_assinatura`. Isto contradiz diretamente §4.1 (*"não são
componentes de topo do envelope"*) e §4.4.1, que os colocam dentro de cada
entrada de `assinaturas[]` desde a ADR-004.

**Resíduo do meu próprio trabalho** — a ADR-004 alterou §4.1/§4.4.1 e o
schema, mas não varreu §2.10.3.

### F5. §6.2 — mesma descrição desatualizada

*"estes campos ficam no envelope, ao mesmo nível de `assinaturas`,
`timestamps` e `validation_code`"* — `timestamps` já não existe a esse nível.
Mesmo resíduo da ADR-004, mesma origem.

### F6. Hierarquia normativa invertida entre `versao_anterior` e `relacoes[substitui]`

- §6.2: `versao_anterior`/`hash_anterior` **DEVEM** estar presentes quando o
  NDF é nova versão de outro.
- §2.11.3: preencher também `relacoes[{tipo: "substitui"}]` é apenas
  **RECOMENDA-SE**, e usar só o envelope é explicitamente **PODE**.

O resultado é que o mecanismo **não assinado** (envelope) é obrigatório e o
mecanismo **assinado e verificável por hash** (core) é opcional — o inverso
da justificação que sustenta a ADR-002 (*"a relação deve estar coberta pela
assinatura porque é parte do sentido do ato"*). Um produtor conforme pode,
hoje, produzir uma cadeia de substituição inteiramente fora dos bytes
assinados.

Não é um erro mecânico: é uma decisão de desenho que ficou incoerente com a
sua própria fundamentação.

---

## Médio — lacunas de definição e cobertura

### F7. Tombstone (§2.4.3) é normativo mas não tem schema

§2.4.3: *"o sistema de custódia DEVE ... criar um registo tombstone imutável
com os seguintes campos mínimos"*, seguido de um exemplo JSON. Não existe
`tombstone.schema.json` nem qualquer outro artefacto que o valide. É o único
requisito estrutural da especificação sem definição verificável por máquina.

Já tinha sido identificado em `docs/design/NDF-STABILIZATION-PROPOSAL.md` §8,
com a recomendação de o representar como `custody-event` com
`event_type: "eliminado"` e os campos em `details` — proposta que nunca foi
executada. Continua a ser a resolução mais económica.

### F8. `versao_anterior`/`hash_anterior` tem cobertura de teste zero

`conformance/ndf/valid/versao-substituicao.json` é apenas um NDF-core, sem
envelope. O `_comment` diz que *"o envelope deste NDF **conteria**
`versao_anterior` + `hash_anterior`"* — descreve em prosa o que nunca é
exercitado. Nenhum caso de conformidade, nenhum `.ndfpkg` de exemplo, nenhum
vetor negativo testa este mecanismo.

Combinado com F3 (manifesto contraditório) e F6 (hierarquia invertida): o
mecanismo está documentado em três sítios, implementado no schema do
envelope, e **nunca verificado por nada**.

### F9. Redundância `versao_anterior` vs `relacoes[substitui]` — decisão em aberto

Os dois mecanismos representam o mesmo facto. O do core é assinado,
verificável por hash, e generaliza para 10 outros tipos de relação. O do
envelope é linear 1:1, não assinado, sem testes, e com a documentação do
manifesto quebrada.

**Opções, para decisão:**

1. **Descontinuar** `versao_anterior`/`hash_anterior`, tornando
   `relacoes[{tipo:"substitui"}]` o mecanismo único. Elimina F3, F6, F8 de
   uma vez. Custo: quebra o schema do envelope (remoção de campos) — mas sem
   consumidores externos, como já estabelecido na ADR-007/ADR-009.
2. **Manter e corrigir**: acrescentar os campos ao manifesto (F3), inverter
   a hierarquia normativa (F6), criar cobertura de teste (F8). Mais trabalho,
   mantém dois mecanismos para o mesmo facto.
3. **Manter como atalho explicitamente derivado**: declarar normativamente
   que `versao_anterior` é uma projeção de `relacoes[substitui]` e que, em
   caso de divergência, o core prevalece.

Recomendo a **opção 1** — é a que melhor serve o princípio já adotado em
toda a revisão anterior (um facto, um sítio, preferencialmente assinado).
Mas é decisão tua: envolve remover um campo publicado.

### F10. Tripla de autoria sem regra de precedência

Três sítios podem afirmar autoria, sem nenhuma cláusula sobre o que
significa divergirem:

| Local | Natureza |
|---|---|
| `participantes[].papel = "autor"` (NDF-core) | índice estrutural, assinado |
| `documento.autor` (`parecer`, `informacao-tecnica`) | campo de exibição do tipo, assinado |
| `assinaturas[].papel = "autor"` (envelope) | quem assinou nessa qualidade, não assinado |

Procura por "divergir/divergem/não coincidir" em `specs/ndf/SPEC.md`: **zero
resultados**.

A assimetria é notória: para `relacoes[]` vs `despacho.sobre[]` criámos uma
regra de coerência (§2.11.4) **e** um aviso no validador (A7). Para a tripla
de autoria — mais suscetível a divergência real, porque envolve três camadas
com propósitos distintos — não há nada. Dois implementadores conformes podem
legitimamente discordar sobre quem é "o autor" de um NDF em que os três
campos apontem para pessoas diferentes.

Não recomendo validação automática de igualdade (são conceitos distintos,
divergir é legítimo). Recomendo **uma cláusula que declare os três como
independentes e defina qual prevalece para efeitos de atribuição de
autoria documental**.

### F11. Campos de schema sem documentação normativa

Existem no schema, ausentes da SPEC:

| Schema | Campos |
|---|---|
| `ndf-core` | `finalidade_detalhe` *(introduzido por mim na ADR-005, nunca documentado em §2.13)* |
| `envelope` | `assinado_em`, `certificado_serie`, `cadeia_certificados`, `revogacao` |
| `custody-event` | `custody_event_version`, `event_id`, `event_type`, `occurred_at`, `actor`, `display_name`, `details` *(consequência de F1)* |

`assinado_em` é o mais relevante: aparece nos exemplos, no schema, e não
consta da tabela de campos de §4.4.1.

---

## Baixo — editorial e manutenção

| # | Achado | Origem |
|---|---|---|
| F12 | §4.1 remete para §4.4.2 ao indicar onde vivem `timestamps`/`validation_material`; a secção correta é §4.4.1 (§4.4.2 é "Preservação da assinatura original") | meu, ADR-004 |
| F13 | §6.2: `****Quando presentes**:` — markdown malformado (4 asteriscos + 2) | pré-existente |
| F14 | §6.2 descreve o tipo de `hash_anterior` como `"sha256:<hex>"`, após a generalização do padrão para `^[a-z][a-z0-9-]*:[0-9a-f]+$` (A9) | meu, ronda A9 |
| F15 | `conformance/ndf/README.md` documenta 14 de 28 casos. 6 omissões são pré-existentes (`modelo3-irs`, `oficio-com-ncrtf`, `document-schema-mismatch`, `mismatched-instrument`, `ncrtf-marks-fora-de-ordem`, `ncrtf-subscript-superscript`); 8 foram introduzidas por mim nas rondas A1–A10 | misto |
| F16 | Enum `estado` (5 valores) duplicado literalmente em `envelope.schema.json` e `manifest.schema.json` — sem mecanismo que impeça deriva entre os dois | pré-existente |

---

## Contagem por origem

Dos 16 achados: **6 são resíduos do meu próprio trabalho** nas rondas
anteriores (F4, F5, F11-parcial, F12, F14, F15-parcial) — sobretudo por não
ter varrido cláusulas secundárias depois de alterar as principais. Os
restantes 10 são anteriores a esta sessão.

O padrão que os une, nos dois casos, é o mesmo: **alterou-se a definição
principal e não se varreram as cláusulas que a citam**. É exatamente o que
esta revisão foi desenhada para apanhar.

---

## O que não encontrei

Registo pela negativa, porque é informação útil para a RC:

- Nenhuma referência `§X.Y` quebrada em nenhuma das quatro SPECs.
- Nenhum caso de conformidade a falhar (58/58).
- Nenhuma incoerência entre `ndf-core.schema.json` e os exemplos que valida.
- Nenhum requisito `NDF-PROD-*`/`NDF-READ-*` sem ID estável ou fora do
  índice gerado.
- Nenhuma dependência de rede ou de runtime NORMORDIS no caminho de
  validação.
- A separação formato↔Perfil de Ciclo de Vida (ADR-010) está consistente nas
  cláusulas que verifiquei, com a exceção já corrigida em §2.10.4.

---

## Sequência recomendada

**Bloco 1 — correções sem decisão (posso executar assim que autorizares):**
F1 (alinhar §2.4.2 ao schema), F2, F4, F5, F11, F12, F13, F14, F15.

**Bloco 2 — exigem decisão tua antes de eu tocar em nada:**

1. **F9** — destino de `versao_anterior`/`hash_anterior`: descontinuar
   (recomendado), corrigir e manter, ou declarar derivado? Resolve F3, F6, F8
   em cascata.
2. **F10** — tripla de autoria: que cláusula de precedência queres?
3. **F7** — tombstone: schema próprio ou `custody-event` com `details`?
4. **F16** — enum `estado` duplicado: aceitar como está, ou consolidar?

**Bloco 3 — depois dos anteriores:** nova passagem dos cruzamentos
automáticos (os scripts ficaram no scratchpad e são reexecutáveis) para
confirmar que nenhuma correção introduziu deriva nova.

Na minha leitura, com o Bloco 1 e as decisões do Bloco 2 aplicadas, o NDF
1.0 fica em condições de ser apresentado como release candidate — não por
estar completo, mas por deixar de conter afirmações que contradizem os seus
próprios artefactos.


---

## Resolução (2026-08-08)

Todos os achados foram fechados. Decisões de fundo tomadas pelo responsável
do projeto; alteração arquitetural registada em **ADR-011**.

| # | Resolução |
|---|---|
| F1 | §2.4.2 alinhada ao `custody-event.schema.json`; semântica antiga (`motivo`, `instrumento_legal`) mapeada para `details` |
| F2 | Exemplo do `manifest.json` em §8.2 completado com os 3 campos obrigatórios em falta |
| F3 | Resolvido por F9 — a afirmação sobre o manifesto foi removida (§2.3, §8.3) |
| F4 | Tabela §2.10.3 corrigida: `timestamps`/`validation_material` são por assinatura |
| F5 | §6.2 reescrita (ver F9) |
| F6 | Resolvido por F9 — deixa de haver dois mecanismos com força normativa diferente |
| F7 | Tombstone → evento terminal `custody-event` com `event_type: "eliminado"`; sem schema novo |
| F8 | Resolvido por F9; `versao-substituicao.json` passa a exercitar `relacoes[substitui]` |
| **F9** | **`versao_anterior`/`hash_anterior` removidos do envelope (ADR-011)** |
| F10 | §2.12.3 nova — três noções de autoria declaradas distintas, com regra de coerência, sem hierarquia de precedência |
| F11 | `assinado_em`, subcampos de `timestamps`/`validation_material`/`revogacao` e `finalidade_detalhe` documentados |
| F12 | §4.1 passa a referir §4.4.1 |
| F13 | Markdown malformado eliminado na reescrita de §6 |
| F14 | Tipo de hash desatualizado eliminado com o campo (F9) |
| F15 | `conformance/INDEX.md` gerado por `tools/build_conformance_index.py`; tabelas manuais removidas do README |
| F16 | Duplicação de enum mantida por decisão; verificação anti-deriva em `tools/check_spec_coherence.py` (C4) |

### Guardrails acrescentados

O padrão que produziu 16 achados — *alterar a definição principal e não
varrer as cláusulas secundárias* — passou a ser verificado automaticamente:

| Verificação | Onde |
|---|---|
| Blocos JSON da SPEC validam contra os schemas | `check_spec_coherence.py` C1 |
| Campos de schema documentados na SPEC | C2 |
| Referências `§X.Y` resolvem | C3 |
| Enums duplicados não derivam | C4 |
| Propriedades removidas por ADR não reaparecem | C5 |
| Índice de conformidade sincronizado com os ficheiros | `build_conformance_index.py` + `git diff --exit-code` em CI |

Ambas as ferramentas estão ligadas a `.github/workflows/validate.yml`.

### Verificação final

```
validate.py                    58/58
--package ndfpkg-example       PASS
check_package_vectors.py       8/8
check_ndt_semantic_corpus.py   9 casos
check_spec_coherence.py        PASS (3 blocos, 105 campos, 164 refs, 1 enum, 2 props removidas)
build_requirements_index.py    54 IDs
audit_normative.py             54 IDs; 186 declarações
build_conformance_index.py     58 casos
check_publication_profile.py   3 drafts
```
