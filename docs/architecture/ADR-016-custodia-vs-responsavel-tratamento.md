# ADR-016: Separação entre custódia do registo e responsabilidade pelo tratamento

**Estado**: Aceite
**Data**: 2026-08-14
**Decisores**: carloscanutocosta

---

## Contexto

`metadados.responsavel_tratamento` é, pelo nome e pela definição em §1.4, o
responsável pelo tratamento na aceção do RGPD (Art.º 13.º–14.º). O schema
exige-o **sempre**, incluindo quando `contem_dados_pessoais: false`, e a SPEC
justifica essa obrigatoriedade com um conceito diferente: §2.7.2 descreve-o como
"identifica o responsável pela custódia do registo".

São conceitos distintos. A custódia institucional de um registo documental
existe em qualquer documento; a responsabilidade pelo tratamento de dados
pessoais só existe quando há dados pessoais, e pode recair sobre entidade
diferente daquela que custodia o registo.

Daqui resultam dois defeitos. O formato obriga a uma declaração RGPD sem facto
RGPD subjacente — um documento que afirma não conter dados pessoais tem de
nomear na mesma um responsável pelo tratamento. E a incoerência inversa não é
detetável: declarar responsável pelo tratamento num documento que afirma não
conter dados pessoais passa hoje sem qualquer erro, porque não existe regra que
o proíba.

Os três campos com semântica exclusivamente RGPD — `categorias_dados_pessoais`,
`base_legal_conservacao` e `responsavel_tratamento` — estão soltos em
`metadados`, ao lado de campos descritivos transversais, com condicionalidade
expressa caso a caso.

## Decisão

1. Criar **`metadados.entidade_responsavel`** (string, obrigatório sempre) — a
   entidade responsável pela custódia do registo. É o conceito que §2.7.2 já
   descrevia, agora com campo próprio.

2. Criar **`metadados.protecao_dados`** (objeto), agrupando os três campos de
   semântica RGPD, com os nomes `categorias`, `base_legal_conservacao` e
   `responsavel_tratamento`. Os três são obrigatórios dentro do bloco.

3. `protecao_dados` é **obrigatório se e só se** `contem_dados_pessoais: true`, e
   **proibido** caso contrário.

4. `contem_dados_pessoais` mantém-se obrigatório. A declaração explícita de
   ausência de dados pessoais não é substituível pela omissão do bloco.

5. Remover de `metadados` os campos `categorias_dados_pessoais`,
   `base_legal_conservacao` e `responsavel_tratamento` ao nível de topo.

## Alternativas consideradas

### Manter `responsavel_tratamento` obrigatório e corrigir apenas a redação

**Prós**: alteração compatível; resolve a confusão conceptual no texto sem tocar
no schema nem em 52 ficheiros.

**Contras**: a confusão não é só de redação — é o campo que está errado. Corrigir
o texto para dizer que `responsavel_tratamento` significa custódia agravaria o
problema, porque o nome do campo continuaria a invocar o RGPD e a ser lido como
tal por qualquer integrador. E não fecharia a incoerência inversa. Rejeitado.

### Tornar `responsavel_tratamento` condicional, sem criar `entidade_responsavel`

**Prós**: alteração menor; elimina a declaração RGPD sem facto RGPD.

**Contras**: perde-se a identificação do custodiante em documentos sem dados
pessoais — informação que §2.7.2 considera necessária e que hoje existe, ainda
que no campo errado. Trocaria um defeito por uma lacuna. Rejeitado.

### Manter os três campos soltos, apenas com condicionalidade corrigida

**Prós**: evita um nível de aninhamento e mantém a forma a que os exemplos já
obedecem.

**Contras**: a condicionalidade teria de ser repetida campo a campo no schema e
no validador semântico, que é onde a regra atual já se dispersa. Agrupar num
bloco torna a regra única — presente ou ausente — e torna exprimível a proibição
do ponto 3, que com campos soltos exigiria três negações separadas. Rejeitado
por preferir uma asserção a três.

### Acrescentar contacto do encarregado de proteção de dados (EPD/DPO)

Considerado por ser informação exigida pelos Art.º 13.º–14.º.

**Contras**: o contacto do EPD muda ao longo do tempo e o NDF-core é imutável —
ficaria desatualizado e não corrigível, o que é pior do que ausente. Cai no
princípio de âmbito de `LACUNAS.md`: não é necessário para reconstituir,
verificar ou interpretar o documento. Pertence ao sistema de gestão, que pode
resolvê-lo a partir de `entidade_responsavel`. Rejeitado.

## Justificação da decisão

A decisão separa dois factos que o formato tratava como um só, e fá-lo no sítio
onde a distinção é verificável: um bloco cuja presença é logicamente equivalente
a `contem_dados_pessoais`. Isso converte uma convenção de redação numa asserção
de schema, e é o que permite detetar a incoerência que hoje passa em silêncio.

A obrigatoriedade de `entidade_responsavel` para todos os documentos preserva o
que a regra atual tinha de correto — há sempre alguém responsável pela custódia
do registo — sem lhe chamar RGPD.

Manter `contem_dados_pessoais` obrigatório, em vez de o inferir da presença de
`protecao_dados`, é deliberado: num documento assinado e imutável, a afirmação
explícita "não contém dados pessoais" é uma declaração com valor probatório,
distinta da simples ausência de informação sobre o assunto. É o mesmo raciocínio
já aceite em ADR-005 para `proveniencia_ia.utilizada: false`.

## Consequências

**Positivas**: elimina a declaração RGPD sem facto RGPD subjacente; torna
detetável a incoerência inversa; agrupa a semântica de proteção de dados num
bloco único, mais fácil de fazer evoluir se a legislação mudar; reduz a três
para uma o número de regras condicionais dispersas no validador.

**Negativas / mitigações**: mais um nível de aninhamento em `metadados`; todos
os exemplos e casos de conformidade têm de ser migrados. Mitigado por a migração
ser mecânica e por ser feita na mesma ronda de ADR-015, que já toca nos mesmos
ficheiros.

**Compatibilidade**: **incompatível**. Absorvido em 1.0.0 antes de qualquer
publicação, ao abrigo de ADR-007 e do estado nível 1 — Draft. Não existe corpo
documental produzido a migrar.

## Referências

- `docs/design/NDF-AVALIACAO-GENERALIZATION.md` §4
- SPEC.md §1.4, §2.7.1, §2.7.2
- ADR-005-proveniencia-ia.md — precedente da declaração explícita de ausência
- ADR-015-generalizacao-avaliacao-arquivistica.md — mesma ronda de alteração
- `LACUNAS.md` — princípio de âmbito
