# Missão — Estabilização NDF para revisão pública e NGI

**Estado:** brief de trabalho (não normativo). Consolida o brainstorming de
2026-08-07 sobre a evolução arquitetural do NDF e integra três emendas
identificadas por confronto direto com o estado real do repositório
(ver [`docs/reports/CURRENT-STATE-ASSESSMENT.md`](../reports/CURRENT-STATE-ASSESSMENT.md)
— Fase 0).
**Não é uma especificação.** É o mandato que orienta a Fase 1
(`NDF-STABILIZATION-PROPOSAL.md`) e as fases seguintes.

---

## Missão

Rever, estabilizar e preparar uma versão publicamente apresentável da
especificação NDF — adequada a revisão técnica externa e, futuramente, a uma
candidatura NGI — incorporando as decisões arquiteturais consolidadas sobre:

1. relações verificáveis entre documentos;
2. processos administrativos compostos por documentos autónomos (Informação →
   Parecer → Despacho);
3. múltiplas assinaturas eletrónicas sobre o mesmo NDF;
4. separação entre autoria, participação, autenticação, assinatura pessoal e
   selo institucional;
5. proveniência e evidência de utilização de IA;
6. suporte técnico à rastreabilidade, transparência e supervisão humana
   previstas no AI Act, sem alegações indevidas de conformidade jurídica;
7. compatibilidade, testes de conformidade e qualidade editorial da
   especificação.

Não tratar esta missão como reescrita total. O repositório já contém uma
especificação madura (SPEC.md com ~1075 linhas normativas para o NDF, schemas
JSON Schema 2020-12, suites de conformidade positivas/negativas, matriz de
rastreabilidade auto-gerada, ADR-001, gates de prontidão honestos). Preservar
o que está correto; alterar incrementalmente, com rastreabilidade explícita.

---

## Princípios arquiteturais obrigatórios

### 1. NDF como fonte documental canónica

O NDF-core representa o documento lógico canónico e imutável. PDF, PDF/A,
PDF/UA, ODF, HTML são projeções derivadas. Canonicalização JCS/RFC 8785; bytes
finalizados nunca reserializados. *(Já normativo — SPEC.md §1.3, §2.1.)*

### 2. Separação entre core e envelope

`NDF-core`: conteúdo lógico e metadados constitutivos, canonicalizados e
assinados. `Envelope`: provas criptográficas, timestamps, material de
validação, informação operacional pós-finalização. Informação necessária para
determinar o sentido ou objeto jurídico-documental do documento — em
particular relações com outros documentos e proveniência essencial de IA —
DEVE entrar no core, não apenas no envelope. *(Já normativo — SPEC.md §1.2;
mas `versao_anterior`/`hash_anterior` estão hoje só no envelope — ver §4.)*

### 3. Documentos administrativos autónomos

Informação, parecer e despacho são documentos autónomos, cada um com
`ndf_id`, tipo documental, conteúdo, participantes, hash, assinaturas,
avaliação arquivística e relações assinadas próprios. Não representar um
parecer ou despacho como assinatura adicional da informação original.

### 4. Relações documentais verificáveis

Introduzir no NDF-core um modelo geral de relações. Cada relação DEVE conter,
no mínimo: tipo de relação, `ndf_id` do alvo, `payload_hash` do alvo — para
que a relação indique não uma identidade lógica genérica, mas os bytes
canónicos exatos sobre os quais incidiu o parecer, despacho, resposta ou
outra ação.

```json
{
  "relacoes": [
    {
      "tipo": "emite_parecer_sobre",
      "alvo": { "ndf_id": "UUID", "payload_hash": "sha256:HEX" },
      "papel": "informacao_base"
    }
  ]
}
```

Registo inicial pequeno e extensível: `substitui`, `corrige`, `complementa`,
`anula`, `responde_a`, `emite_parecer_sobre`, `decide_sobre`, `executa`,
`anexa`, `deriva_de`, `referencia`. Não criar uma ontologia administrativa
extensa nesta versão; documentar como se estende sem colisão semântica
(registo versionado ou identificadores qualificados).

**Emenda — vocabulário de proveniência (PROV-O).** Documentar o mapeamento de
cada tipo de relação para a primitiva equivalente do PROV-O (W3C), quando
exista correspondência natural: `substitui` → `prov:wasRevisionOf`,
`deriva_de` → `prov:wasDerivedFrom`, `emite_parecer_sobre`/`decide_sobre` →
`prov:wasInformedBy`, `corrige`/`complementa`/`anula`/`responde_a`/`executa`/
`anexa`/`referencia` → mapear caso a caso ou marcar como extensão sem
equivalente direto. Isto não obriga a serializar em PROV-O — apenas ancora a
semântica num vocabulário de proveniência já testado, para interoperabilidade
futura fora do ecossistema NORMORDIS.

**Migração de `versao_anterior`/`hash_anterior`.** Hoje vivem só no envelope
(`envelope.schema.json`), não cobertos pela assinatura. Avaliar migração para
o novo modelo de relações no core (`tipo: "substitui"`), com estratégia
explícita — manutenção temporária, depreciação, mapeamento, ou nova versão
major/minor conforme `VERSIONING.md`. Não eliminar compatibilidade
abruptamente.

**Nota de reconciliação (relações já existentes de facto).** O schema
`specs/registry/schemas/despacho.schema.json` já tem um campo `documento.sobre[]`
com `{ndf_id, descricao}` — sem `payload_hash`, dentro de `documento` (não no
NDF-core genérico), e específico do tipo `despacho`. É a evidência mais
concreta de que a necessidade é real, mas confirma exatamente a fragilidade
apontada: falta o hash e falta ser um mecanismo genérico reutilizável por
qualquer `tipo_documento_ref`. Ao desenhar `relacoes[]` no core, decidir e
documentar explicitamente a relação entre os dois mecanismos (substituir
`sobre[]`, mantê-lo como atalho de leitura derivado de `relacoes[]`, ou
descontinuá-lo com plano de migração).

### 4bis. Retenção, destino final e eliminação — já em grande parte coberto

**Não tratar como lacuna a preencher do zero.** O NDF-core já tem um bloco
`avaliacao` completo (PCA, `destino_final` ∈ {`conservacao_permanente`,
`eliminacao`, `conservacao_parcial_por_amostragem`}, referência ao instrumento
DGLAB/PGD/Portaria — SPEC.md §3), um ciclo de vida arquivístico operacional
(`estado` no envelope: `ativo → em_conservacao → conservado_permanentemente |
eliminado` — §2.4.1) e um **mecanismo de tombstone já especificado** (§2.4.3:
ao eliminar, destroem-se `payload_bytes` e o envelope exceto
`validation_code`/`payload_hash`, e cria-se um registo tombstone imutável com
`data_eliminacao`, `motivo_eliminacao`, `instrumento_avaliacao_versao_ref`).
A tensão imutabilidade↔RGPD já está tratada em §1.4 com o mesmo raciocínio
que motivou esta emenda (base legal de conservação, pseudonimização,
eliminação no termo do PCA).

O trabalho real aqui é de **integração**, não de criação: garantir que o novo
bloco `relacoes[]` e o modelo de participantes/assinaturas não colidem com
este mecanismo já maduro, e que uma relação `anula`/`substitui` proveniente de
outro NDF é coerente com uma transição de `estado` para `substituido`
decidida pelo sistema de custódia. Verificar também se `custody-event.schema.json`
(`event_type` enum) precisa de um valor dedicado quando a transição resulta de
uma relação `anula` explícita vindo de outro documento, distinto de
`estado_alterado` genérico — avaliar, não assumir que é necessário.

### 5. Participantes e autoria

Distinguir autor, coautor, revisor humano, validador, aprovador, decisor,
representante, entidade produtora, sistema técnico interveniente — sem
confundir com assinatura eletrónica. Hoje esta informação está fragmentada e
sem modelo comum: `autor` em `informacao-tecnica.schema.json`, `decisor` em
`despacho.schema.json`, `signatario` no envelope — três representações de
identidade não coordenadas entre si. Preferir identificadores institucionais
estáveis, dados mínimos no core.

### 6. Múltiplas assinaturas

`envelope.assinaturas[]` já existe e já é um array (`envelope.schema.json`
`$defs.assinatura`). Dois problemas concretos confirmados na leitura do
schema atual, a resolver:

- `timestamps` e `validation_material` estão ao nível global do envelope, não
  por assinatura — com N assinaturas independentes (certificados, cadeias,
  OCSP/CRL e timestamps potencialmente distintos), a associação prova↔
  assinatura fica ambígua. Cada assinatura deve tornar-se unidade de prova
  autocontida (`assinatura_id`, `validation_material` e `timestamps` próprios).
- `signatario` tem `nome`, `certificado_serie`, `cargo` — mas não distingue
  cargo organizacional de **papel exercido naquele documento** (`autor`,
  `coautor`, `validador`, `aprovador`, `decisor`, `representante`,
  `testemunha`, `selante`), nem tem `ordem` para coautoria/sequência.

Não transformar o NDF num motor de workflow: papel e ordem são descritivos do
resultado assinado, não uma máquina de estados de aprovação — isso pertence
ao sistema de workflow, fora desta especificação. Não atribuir personalidade
jurídica, autoria ou capacidade de assinatura a sistemas de IA.

### 7. Proveniência de IA

Bloco opcional no NDF-core, só necessário quando a IA influenciou
materialmente o conteúdo. Dois níveis: proveniência essencial no core
(finalidade, sistema/fornecedor/modelo/versão, data, resultado incorporado,
segmentos afetados, estado da revisão humana, revisor, referência+hash da
evidência externa) e logs detalhados (prompts integrais, respostas completas)
fora do NDF, com política própria de acesso/retenção. Não tornar obrigatória
a inclusão de prompts integrais.

### 8. AI Act

Não afirmar que um NDF, por si só, é "conforme com o AI Act". Formulação a
adotar, consistente com o tom já usado em todo o SPEC.md atual (ex.: §1.1 —
"a conformidade jurídica depende da implementação, certificados, políticas,
contexto de utilização e legislação aplicável; não são garantidas pelo
formato isoladamente" — o mesmo padrão de redação cautelosa aplicado ao RGPD
já existe e deve ser replicado para IA):

> O NDF fornece mecanismos técnicos que podem apoiar rastreabilidade,
> transparência, supervisão humana e conservação de evidências relativas ao
> uso de sistemas de IA. A conformidade jurídica depende do sistema,
> finalidade, classificação de risco, operadores, contexto jurídico e medidas
> técnicas e organizativas aplicáveis.

Considerar um documento informativo dedicado,
`docs/normalization/AI-PROVENANCE-GUIDANCE.md`, no mesmo espírito de
`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md` já existente.

### 9. Informação → Parecer → Despacho

Criar exemplo completo com três NDF (três `ndf_id`, três hashes, tipos
documentais distintos, participantes distintos, relações tipadas e assinadas,
despacho referenciando informação e parecer). **Nota de estado**: o registo
(`specs/registry/schemas/`) já tem `informacao-tecnica` e `despacho`, mas
**não existe ainda schema `parecer`** — é preciso criar este terceiro tipo
para o exemplo ficar completo. Incluir casos inválidos (relação sem
`ndf_id`/`payload_hash`, hash mal formatado, tipo de relação fora do perfil
fechado, revisão humana declarada concluída sem revisor/data, etc.).

### 10. Compatibilidade e versionamento

Ler `VERSIONING.md`, `CONFORMANCE.md`, `GOVERNANCE.md`, ADR-001 e os demais
documentos de `docs/normalization/` antes de alterar schemas. Como
`ndf-core.schema.json` usa `additionalProperties: false`, acrescentar campos
é incompatível para leitores 1.0.0 — decidir formalmente entre NDF 1.1.0,
2.0.0 ou extensão, com análise de compatibilidade, não por intuição.

**Emenda — agilidade de hash.** `payload_hash_alg` já é um enum pensado para
evoluir (hoje fixo a `["sha256"]`, com nota explícita em SPEC.md §2.5 de que
suporte multi-algoritmo está previsto para 1.2.0) — este ponto está bem
desenhado. O que **não** está agilizado é o **formato da própria string de
hash**: `payload_hash`, `hash_anterior`, e (potencialmente) o novo
`relacoes[].alvo.payload_hash` usam todos o padrão fixo
`^sha256:[0-9a-f]{64}$` em `envelope.schema.json`, `manifest.schema.json` e
`custody-event.schema.json`. Avaliar generalizar para
`^[a-z0-9-]+:[0-9a-f]+$` já nesta ronda — para o campo novo `relacoes[].alvo.payload_hash`
não nascer com a mesma rigidez que se terá de corrigir mais tarde em 1.2.0.
Marcar como `DECISION REQUIRED` por ser mudança de padrão com efeito de
compatibilidade em múltiplos schemas.

**Janela de revisão pública em curso.** `docs/normalization/REVIEW-LOG.md`
regista PR-001 (NDF 1.0.0, NDT 2.0.0, NCRTF 2.0.0) com período
2026-07-01–2026-08-15, estado atual `preparação`. À data de hoje (2026-08-07)
essa janela está tecnicamente a decorrer. Marcar como `DECISION REQUIRED`:
confirmar com o maintainer se PR-001 já está formalmente aberta e, em caso
afirmativo, se as alterações desta missão devem aguardar o fecho da revisão
em curso, correr em paralelo como proposta candidata a 1.1.0, ou serem
tratadas como parte da própria preparação da revisão (o estado `preparação`
sugere que pode ainda não ter sido publicamente aberta).

### 11. Schemas

Manter JSON Schema Draft 2020-12, `additionalProperties: false` em estruturas
normativas fechadas, IDs versionados, exemplos coerentes. Preferir schemas
modulares com `$ref`. Evitar enums gigantes prematuros, texto jurídico dentro
de schemas, datas sem timezone.

### 12. Conformidade

Ampliar `conformance/ndf/` (hoje 6 casos válidos / 14 inválidos) com casos
para relações, múltiplas assinaturas, proveniência de IA e compatibilidade de
versões. Fixtures artificiais devem ser marcadas explicitamente como
sintéticas — nunca declarar o gate CAdES concluído com blobs base64
fabricados (`READINESS.md` já identifica isto honestamente como gate externo
pendente; não regredir essa honestidade).

### 13. Segurança e privacidade

Cobrir: ciclos no grafo documental, relações para `ndf_id` inexistentes,
ataques de substituição, path traversal e zip bombs no `.ndfpkg` (o manifesto
já valida `ficheiro` contra `^(?!/)(?!.*\.\.)[A-Za-z0-9._@/-]+$` — confirmar
que o novo trabalho não introduz uma via de contorno), disclosure excessivo
de prompts de IA, controlo de acesso a evidências externas.

### 14. Qualidade pública e NGI

Descrição-alvo do README (ajustar tom, não transformar em marketing):

> O NDF representa cada documento como um nó imutável e verificável de um
> grafo documental. Conteúdo, proveniência e relações são preservados como
> dados canónicos; assinaturas e evidências criptográficas são transportadas
> num envelope separado; PDF, ODF e HTML são projeções interoperáveis.

### 15. ADRs e rastreabilidade

Registar ADRs (seguindo o formato de `ADR-001-json-not-xml.md`, hoje o único
existente) para: relações documentais no core; documentos autónomos vs.
secções sucessivamente assinadas; material de validação por assinatura;
proveniência essencial de IA no core + logs externos; participantes vs.
signatários; estratégia de versionamento/compatibilidade.
`REQUIREMENTS.md` e `NORMATIVE-STATEMENTS.md` são **gerados** por
`tools/build_requirements_index.py` e `tools/audit_normative.py` — não editar
manualmente; qualquer novo **DEVE**/**NÃO DEVE** no texto do SPEC.md com o
formato de ID existente (`NDF-PROD-0NN`, etc.) é apanhado automaticamente ao
correr essas ferramentas.

---

## Decisões confirmadas (Fase 1 → Fase 2)

Confirmado pelo utilizador em 2026-08-07, resolvendo os dois pontos
`DECISION REQUIRED` de `NDF-STABILIZATION-PROPOSAL.md` §11:

1. Manter `ndf_version: "1.0.0"` — sem bump. Formato criado de raiz, sem
   revisão pública ainda aberta.
2. Não existe nenhum consumidor/implementação externa do NDF hoje —
   liberdade total para reestruturar o modelo de assinatura do envelope
   (mover `timestamps`/`validation_material` para dentro de cada
   `assinatura`) sem preocupação de compatibilidade retroativa.

## Método de trabalho

Fase 0 (inspeção) → Fase 1 (proposta arquitetural,
`docs/design/NDF-STABILIZATION-PROPOSAL.md`) → Fase 2 (implementação) →
Fase 3 (verificação) → Fase 4 (relatório,
`docs/reports/NDF-STABILIZATION-REPORT.md`). Ver detalhe de cada fase no
brainstorming original desta missão (registado na conversa que originou este
documento). Fase 0 está concluída — ver
[`docs/reports/CURRENT-STATE-ASSESSMENT.md`](../reports/CURRENT-STATE-ASSESSMENT.md).

## Restrições

Não publicar, não fazer push, não abrir PR, não criar release sem autorização
explícita. Não alterar licenças. Não declarar homologação, certificação ou
conformidade jurídica. Não simular revisão jurídica/arquivística/criptográfica
independente. Não marcar gates externos como concluídos. Não usar assinaturas
sintéticas como evidência CAdES real. Não tornar NDF dependente do runtime
NORMORDIS. Não introduzir dependência de fornecedor. Não guardar
obrigatoriamente prompts integrais no NDF. Não permitir IA como signatário
pessoal. Não colocar relações documentais apenas no envelope. Não alterar
schemas publicados sob o mesmo `$id` de forma incompatível e silenciosa.
Manter língua normativa em português europeu.

## Critérios de conclusão

1. Informação → Parecer → Despacho representado por NDF autónomos e relações
   verificáveis.
2. Cada relação relevante coberta pelo NDF-core assinado.
3. Várias assinaturas coexistem sem ambiguidade de certificados, timestamps
   ou material de validação.
4. Autoria, participação, papel administrativo, assinatura e selo
   distinguidos.
5. Proveniência de IA proporcional, verificável, minimizada.
6. Documentação não promete conformidade automática com o AI Act.
7. Schemas, SPEC, exemplos e testes sincronizados.
8. Versão e compatibilidade formalmente justificadas.
9. Suites passam ou falhas documentadas.
10. Gates externos continuam visíveis (não artificialmente fechados).
11. Um terceiro compreende e testa a proposta sem conhecimento prévio do
    NORMORDIS.
12. Relatório final honesto, adequado a revisão pública.
