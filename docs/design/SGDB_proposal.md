# Proposta de armazenamento em SGBD — perfil de custódia

**Estado:** estudo de desenho, não normativo. Nenhuma decisão aqui registada
altera uma especificação enquanto não for aprovada e vertida para a SPEC
respetiva. Este documento não substitui `docs/architecture/ARCHITECTURE.md`
nem `docs/benchmarks/STORAGE.md` — desenvolve o que ambos já pressupõem.

**Origem:** discussão sobre `participantes[].evidencia_acao` (SPEC.md §2.12.8)
e a necessidade, levantada pelo responsável do projeto, de registar
conceptualmente a adequação do NDF a um SGBD — a par da reconstrução
determinística já documentada — como parte do que demonstra utilidade prática
do formato.

**Objetivo:** explicar como um SGBD concreto (relacional, documental, ou
armazenamento de objetos) pode implementar o **perfil de custódia** definido
em `ARCHITECTURE.md` §4, cumprindo os três requisitos que essa secção já
impõe — resolução **transacional, imutável e auditável** — sem comprometer a
canonicalização JCS de que depende toda a cadeia de integridade do NDF.

---

## 0. Porque isto importa para a utilidade demonstrada do formato

`ARCHITECTURE.md` §1 já documenta, em dois diagramas separados, um lado do
ciclo de vida do NDF — produção (`editor`/`NCRTF`/`NDF-core`/`NDT` →
`renderizador` → PDF/ODF/HTML) e empacotamento (`NDF-core + envelope + NDT +
schemas + recursos` → `.ndfpkg`). Lidos em conjunto — um `.ndfpkg` contém
exatamente o que um renderizador precisa —, sintetizam-se numa única cadeia:

```text
NDF-core + envelope + NDT + schemas + recursos ──► .ndfpkg
                                                 ──► renderizador ──► PDF / ODF / HTML / …
```

Este é o lado da **projeção**: de dados estruturados e imutáveis para uma
representação visual. É meio da história. A outra metade — sem a qual a
primeira não tem onde viver — é: **como é que os bytes canónicos chegam
íntegros do momento da finalização até ao momento em que alguém pede a
reconstrução, possivelmente anos depois, através de um SGBD que nunca foi
desenhado a pensar em JCS?**

Um formato que só demonstra "sei serializar e assinar um documento" não
convence uma equipa de engenharia a adotá-lo; um formato que também mostra
"aqui está como isto vive dentro do Postgres/Mongo/MinIO que já tens, sem
quebrar a prova" fecha o argumento de adoção. Este documento existe para essa
segunda metade.

## 1. O ponto crítico transversal — JCS não sobrevive a um SGBD por omissão

O NDF exige RFC 8785 (JCS) para tudo o que é canonicalizado, hashed ou
assinado — `payload_hash` (calculado em SPEC.md §5.2; o algoritmo é
declarado em §2.5) e a própria admissibilidade da suite de conformidade
(R17, `tools/check_jcs_required.py` recusa arrancar sem isso). Isto tem uma
implicação direta para qualquer SGBD: **o que é hash e assinado são bytes
exatos, não "o mesmo conteúdo lógico".**

- **PostgreSQL `jsonb`** decompõe o JSON num formato binário interno: pode
  reordenar chaves, normaliza espaços e reformata números. Reconstituir JSON
  a partir de `jsonb` **não** reproduz garantidamente os mesmos bytes que
  foram canonicalizados e assinados.
- **MongoDB (BSON)** preserva a ordem de inserção das chaves, mas a
  codificação de números (`int64`/`double` do BSON) não segue as regras
  específicas do JCS para `ToString` de números — outra fonte de divergência
  silenciosa, mais difícil de detetar do que a reordenação de chaves porque o
  documento parece "igual" a olho nu.

**Regra prática, para qualquer SGBD escolhido:** o NDF-core canonicalizado (os
bytes que foram *hashed*) é guardado como um blob opaco — `bytea`/`text` em
Postgres, `BinData` em Mongo — nunca reconstituído a partir de uma
representação decomposta. `jsonb`/BSON servem só como **cópia derivada,
indexável, para consulta** — nunca como fonte de verdade para verificação de
hash ou assinatura. Esta não é uma particularidade do NDF: é a mesma armadilha
que já existe para qualquer formato canonicalizado (XML-C14N tem o mesmo
problema com serializadores XML "bem comportados" que decidem reformatar).

## 2. A fronteira que a própria especificação já fixa

Duas peças já existentes reduzem este estudo a "escolher a tecnologia dentro
de uma fronteira já fixada", não a desenhar de raiz:

- **`ARCHITECTURE.md` §4 — perfil de custódia vs. perfil portátil.** O perfil
  de custódia já é definido como "armazenamento em base de dados do NDF-core
  canónico e envelope; NDTs, schemas, certificados e recursos podem ser
  deduplicados por hash dentro do domínio de custódia, desde que a resolução
  seja transacional, imutável e auditável." Este documento detalha como
  cumprir esses três adjetivos.
- **SPEC.md §2.4.2 e §4.7.** O log de auditoria de custódia tem de ser
  "separado do NDF e da sua base de dados operacional"; e a cifra, o controlo
  de acesso e a topologia de armazenamento são responsabilidade do sistema de
  custódia, nunca do formato (§4.7). Nenhum SGBD "resolve conformidade NDF"
  por si só — resolve, quando bem configurado, a parte que a SPEC
  deliberadamente deixa em aberto.

Juntando as duas peças: o modelo já pressuposto tem **três camadas**, não uma
tabela única —

1. bytes canónicos do NDF-core + envelope (perfil de custódia, imutável);
2. log de custódia/auditoria (append-only, cadeia de hash — SPEC.md §2.4.2);
3. base de dados operacional (workflow, índices, pesquisa — explicitamente
   separada de (2) por §2.4.2).

## 3. Opção A — Relacional (PostgreSQL)

**Onde encaixa bem:**

- **Transações ACID** para o pipeline de finalização (SPEC.md §5.2, passos
  estritos) — um `BEGIN`/`COMMIT` que só confirma depois de canonicalização,
  hash e `validation_code` estarem consistentes satisfaz literalmente o
  requisito "transacional" de `ARCHITECTURE.md` §4.
- **Consulta estruturada** sobre `participantes[].participante_ref`,
  `imputacao[].imputado.ref`, `avaliacao.destino_final`/`prazo_conservacao` —
  "todos os documentos imputados ao NIF X" ou "elegíveis para eliminação em
  2027" é SQL simples com tabelas normalizadas, e escala melhor do que
  `jsonb @>` em volume alto.
- **`avaliacao.prazo_conservacao`/`destino_final`** (SPEC.md §3) mapeiam
  diretamente para lógica de retenção agendada — particionamento por ano de
  `data_documento` (`pg_partman`), jobs SQL para sinalizar elegibilidade de
  eliminação.
- **"Imutável" e "auditável"** aproximam-se por política: revogar
  `UPDATE`/`DELETE` do papel aplicacional numa tabela, com um trigger que só
  permite `INSERT`, simula o *append-only* que §2.4.2 exige para o log de
  custódia. É imposição de política, não impossibilidade física — diferença
  que a própria SPEC assinala em §9.5 (Perfil de Ciclo de Vida NORMORDIS,
  opcional, onde WORM real é discutido).
- A **cadeia de hash do log de custódia** (§2.4.2) mapeia bem para uma tabela
  com `event_hash`, `previous_event_hash` e uma restrição que impede
  reescrita silenciosa de uma entrada intermédia.

**Onde exige cuidado:**

- Schema relacional rígido vs. tipologia documental extensível
  (`tipo_documento_ref`, schemas versionados no registo — SPEC.md §2.9.2): a
  resposta correta é **não** normalizar `documento` (o conteúdo do tipo) em
  colunas — fica em `jsonb` (só para consulta) mais o blob canónico (para
  prova). Só os campos estáveis do NDF-core (`ndf_id`, `estado`,
  `nivel_assinatura`, `metadados.*`) valem a pena como colunas nativas.
- JSON Schema Draft 2020-12 não é nativamente aplicável em Postgres — a
  validação estrutural fica sempre na aplicação (`tools/validate.py` já faz
  isto); o SGBD garante só a integridade referencial e dos dados extraídos.

## 4. Opção B — Documental NoSQL (MongoDB e afins)

**Onde encaixa bem:**

- Fit imediato: o NDF-core **já é** um documento JSON canónico — inserir o
  payload inteiro como documento é natural, sem "achatar" nada.
- `$jsonSchema` como validador nativo — primeira barreira útil, mas com
  suporte parcial a `$ref`/`$defs` e a `if`/`then`/`else` face ao Draft
  2020-12 do NDF: **não substitui** `tools/validate.py`.
- Transações multi-documento (desde a 4.0) cobrem o mesmo requisito
  "transacional" que o Postgres, para o pipeline de finalização.

**Onde exige cuidado:**

- `relacoes[]` (SPEC.md §2.11) e sucessão documental (§6) são grafo, não
  árvore — `$graphLookup` funciona mas degrada mal com profundidade/volume;
  um `WITH RECURSIVE` em Postgres tende a bater isto para grafos documentais
  complexos.
- Consulta agregada sobre `imputacao`/`participantes` a alto volume tende a
  precisar de índices secundários manualmente geridos; em Postgres o mesmo
  padrão sai "de fábrica" com chaves estrangeiras e índices B-tree.

## 5. O modelo que a arquitetura já sugere com mais força — objeto imutável + índice separado

Dado que `ARCHITECTURE.md` §4 e SPEC.md §2.4.2/§4.7 já pressupõem separar
"bytes do perfil de custódia" de "base de dados operacional", o modelo mais
fiel ao desenho do NDF não é um SGBD único, é híbrido:

- **Armazenamento de objetos com WORM real** (Object Lock em S3/MinIO ou
  equivalente) para os bytes canónicos do NDF-core e do envelope —
  endereçados pelo próprio `payload_hash`/`validation_code`. Isto dá
  imutabilidade **física**, não simulada por permissões de SGBD — satisfaz o
  adjetivo "imutável" sem depender de disciplina operacional contínua.
- **SGBD relacional ou documental só para o índice operacional**: metadados
  extraídos, `participantes`, `imputacao`, estado do workflow, e o log de
  custódia como tabela/coleção *append-only* com a cadeia de hash de §2.4.2 —
  satisfaz "transacional" e "auditável".
- **Deduplicação de NDT/schemas/certificados por hash**, exatamente como
  `ARCHITECTURE.md` §4 já permite, dentro do mesmo armazenamento de objetos
  ou num cache de aplicação — ver `docs/benchmarks/STORAGE.md`, secção "custo
  amortizado", que já mede este ganho (62 KB de schemas pagos uma vez, não
  por documento).

Este modelo não é uma invenção deste documento: é a explicitação, com
tecnologias concretas, do que a ARCHITECTURE.md já definia em prosa.

## 6. Instanciação ilustrativa — não normativa, não vinculativa

O `ndf-core` é agnóstico de SGBD por desenho (`ARCHITECTURE.md` §1: "As
especificações são agnósticas de linguagem, runtime, base de dados e
fornecedor"). A tabela abaixo é **um exemplo de instanciação**, não uma
recomendação do formato em si — serve para tornar concreto o modelo da
secção 5 usando componentes reais, sem que isso implique que o NDF exige
qualquer um deles:

| Camada do perfil de custódia | Componente ilustrativo | Papel |
|---|---|---|
| Bytes canónicos (NDF-core, envelope) | Armazenamento de objetos com Object Lock | Imutabilidade física, endereçada por hash |
| Índice operacional (`participantes`, `imputacao`, `avaliacao`, workflow, `evidencia_acao`) | SGBD relacional | Consulta estruturada, retenção agendada, transacionalidade do pipeline de finalização |
| Log de custódia (§2.4, cadeia de hash) | Tabela *append-only* no mesmo SGBD relacional, schema/role distintos do índice operacional | Separação lógica de §2.4.2, sem exigir um segundo SGBD |
| Eventos de workflow (ex.: "revisão confirmada" → grava `evidencia_acao`) | Fila de mensagens | Desacopla a ação humana no GED do momento em que é persistida no NDF |
| Cache de resolução de `validation_code` (§4.6.4) | Cache em memória | Só se existir serviço de verificação exposto — nunca como fonte de verdade |

Um SGBD documental entra nesta tabela se o sistema que consome o NDF já for
documental por outras razões operacionais — não há vantagem específica do
NDF-core em si que o justifique sobre a opção relacional.

## 7. Checklist de armadilhas, independente da escolha final

1. Nunca fazer *hash*/assinar a partir de `jsonb`/BSON reconstituído — só a
   partir do blob canónico armazenado (§1 acima).
2. `participante_ref`/`imputado.ref` são referências opacas por desenho
   (SPEC.md §2.12.4, §2.15.2) — não as transformar em chave estrangeira para
   uma tabela de identidade dentro do mesmo SGBD do NDF; a resolução fica no
   sistema produtor, como a SPEC insiste.
3. O log de custódia tem de poder ser **exportado integralmente** para outra
   entidade (SPEC.md §2.4.4, `CUST-REQ-004`) — evitar acoplá-lo a
   funcionalidades proprietárias do SGBD que dificultem essa portabilidade.
4. Nenhum SGBD valida o JSON Schema Draft 2020-12 do NDF de forma completa e
   nativa — `tools/validate.py` (ou equivalente na aplicação) continua a ser
   o único guardião real da conformidade estrutural, seja qual for a
   tecnologia de persistência.
5. A deduplicação de NDT/schemas (`ARCHITECTURE.md` §4) é uma otimização
   física — uma exportação para perfil portátil (`.ndfpkg`) tem sempre de
   **reconstituir todos os objetos**, nunca assumir que o recetor tem acesso
   ao mesmo domínio de custódia.

## 8. Ligação ao outro lado do ciclo — reconstrução determinística

O valor prático do formato não está só em "guarda-se sem corromper", mas em
"guarda-se sem corromper **e** continua a produzir, deterministicamente, a
mesma representação visual". Um sistema que implemente o perfil de custódia
conforme este documento fecha o ciclo completo:

```text
finalização ──► perfil de custódia (SGBD, §5–6 acima) ──► leitura anos depois
                                                        ──► .ndfpkg (perfil portátil)
                                                        ──► renderizador ──► PDF/A / ODF / HTML
```

Se os bytes canónicos sobreviverem intactos ao SGBD (secção 1), a
reconstrução determinística já documentada em `ARCHITECTURE.md` §1 continua
válida no momento da leitura, independentemente de quanto tempo passou ou de
quantas migrações de SGBD ocorreram entretanto. É esta cadeia — armazenamento
íntegro **mais** projeção determinística — que demonstra utilidade real do
NDF, não cada metade isoladamente.

## Em aberto

- Medir, sobre um corpus real em Postgres (não só estimativas de tamanho —
  `docs/benchmarks/STORAGE.md` já mede bytes, falta medir tempo de escrita/
  leitura transacional a volume).
- Decidir se o log de custódia *append-only* justifica uma extensão dedicada
  (ex.: `pgaudit`, ou uma tabela particionada por ano) antes de qualquer
  implementação de referência ser publicada.
- Este documento não cobre cifra em repouso nem gestão de chaves — mantém-se
  deliberadamente fora de âmbito, como SPEC.md §4.7.1 já determina.
