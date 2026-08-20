# ADR-023: Quarto modo do invariante de origem — origem não apurável

**Estado**: Aceite
**Data**: 2026-08-20
**Decisores**: carloscanutocosta

---

## Contexto

§2.2.1 exige que todo o NDF declare uma origem identificável do conteúdo, por um
de três modos: `participantes` com papel de autoria, `proveniencia_sistema`, ou
`proveniencia_ia.utilizada: true`. A cláusula acrescenta, expressamente, que «o
invariante não obriga a inventar informação».

Enquanto todo o NDF nascia no sistema produtor, os três modos bastavam: a origem
era sempre conhecida. A captura de documentos (§2.8.1, ADR-020) tornou real um
caso que antes não existia — **um documento pode entrar em custódia sem que a
sua origem seja apurável**.

Três casos concretos, nomeados nos termos do ADR-015:

1. documento em papel digitalizado, de 1987, sem menção de autor nem de serviço;
2. denúncia anónima, que é documento administrativo e de conservação obrigatória;
3. ficheiro recebido de sistema de terceiro sem identificação de origem.

Nenhum dos três modos os cobre. `metadados.entidade_produtora` existe e
identifica a entidade a que o documento é atribuído, mas **não satisfaz o
invariante**, e `participantes` admite apenas pessoas singulares.

O resultado é que §2.2.1 obriga, nestes casos, a rejeitar o documento — ou a
fabricar um autor, que a própria cláusula proíbe.

## Decisão

Um quarto modo: `metadados.origem_nao_identificavel`, com `fundamento`
obrigatório.

```json
{
  "metadados": {
    "origem_nao_identificavel": {
      "fundamento": "Documento em papel digitalizado, sem menção de autor nem de serviço emissor."
    }
  }
}
```

O `anyOf` do schema do NDF-core ganha um quarto ramo. O bloco **NÃO DEVE**
coexistir com uma declaração que identifique a origem — `participantes` com
`papel` em `autor`, `coautor` ou `decisor`, ou `proveniencia_sistema` não vazio
—, e o schema rejeita a combinação.

**Pode** coexistir com `proveniencia_ia`: a intervenção de IA num documento
capturado é tipicamente assistência — classificação, extração, sumarização — e
não produção do conteúdo. As duas declarações são então simultaneamente
verdadeiras.

## Alternativas consideradas

### Recusar documentos de origem não apurável

É o estado anterior a este ADR. Significa que uma denúncia anónima ou um
documento digitalizado sem autor não podem ser NDF — logo, não podem ser
custodiados pelo mecanismo que o projeto propõe para custodiar documentos.
O caso é real, frequente e de conservação obrigatória.

### Fabricar um autor ou um sistema

`participantes` com um `participante_ref` genérico, ou `proveniencia_sistema`
declarando o sistema de ingestão como produtor. As duas são falsas: o sistema de
ingestão não produziu o conteúdo, e não há pessoa a nomear. §2.2.1 proíbe-o
expressamente, e com razão — um invariante satisfeito por informação inventada
deixa de ser um invariante.

### Novo bloco de topo no NDF-core

Falha o passo 3 do teste de admissão: `metadados` é o bloco dos campos
descritivos transversais, e «a origem deste documento não é apurável, pela razão
X» é facto descritivo transversal. Crescer o topo do core quando um bloco
existente absorve o caso é exatamente o que o teste evita.

### Deixar o campo sem `fundamento` obrigatório

Seria uma via de fuga: bastaria declarar o bloco vazio para dispensar qualquer
origem, e o invariante passaria a ser facultativo na prática. Com `fundamento`
obrigatório, a declaração é uma afirmação concreta que alguém assume, que entra
nos `payload_bytes` e que a assinatura cobre.

## Justificação da decisão

**O teste de admissão de novas primitivas** (`ROADMAP.md`, 2026-08-15) dá seis
respostas coerentes: é informação documental; não cabe em `documento`, porque o
invariante é regra de nível core e um schema de tipo não pode satisfazer um
`anyOf` do core; **cabe em `metadados`**; não é variação jurisdicional; não pode
viver fora do NDF, porque o invariante impõe-se estruturalmente dentro do core;
e não pode simplesmente não existir, porque os três casos são reais.

**É o padrão que o formato já usa três vezes** para tornar a ausência
representável em vez de omitida: `revisao_humana.estado: "pendente"` (§2.13.3),
`destino_final: "a_determinar"` (§3.4.1) e `reconstituicao.estado: "ausente"`
(schema de `documento-capturado`). Um formato que só sabe exprimir o que se sabe
obriga quem o usa a mentir sobre o que não sabe.

**É também o que [ADR-022](ADR-022-dever-do-formato.md) exige.** O dever do
formato é permitir que toda a informação relevante e necessária possa ser
guardada. «A origem deste documento não é apurável» é informação relevante — e
não tinha onde ser guardada.

## Consequências

**Positivas**: documentos de origem não apurável passam a ser custodiáveis sem
falsificação. A declaração é explícita, fundamentada, assinada e filtrável — um
sistema pode listar todos os documentos cuja origem não foi apurada, o que antes
não era possível porque não existiam.

**Negativas / mitigações**: o modo pode ser usado por comodidade, para evitar o
trabalho de apurar a origem. A mitigação é o `fundamento` obrigatório — obriga a
escrever a razão, e uma razão escrita é auditável e contestável, ao contrário de
um campo omitido. A exclusão mútua com os modos identificados impede o outro
abuso: declarar as duas coisas para satisfazer o invariante por qualquer via.

**Alteração ao NDF-core.** Ao contrário do alargamento de §2.8, esta decisão
altera o schema do core: propriedade nova em `metadados` e ramo novo no `anyOf`.
Está registada como decisão de âmbito no [`ROADMAP.md`](../../ROADMAP.md).
`ndf_version` mantém-se em `1.0.0` (ADR-007): a adição é opcional e não invalida
nenhum documento existente.

## Referências

- SPEC.md §2.2.1 (invariante de origem), §2.7.6 (o bloco), §2.8.1 (captura), §2.12.2 (papéis)
- [`ROADMAP.md`](../../ROADMAP.md) — teste de admissão (2026-08-15); decisão de âmbito (2026-08-20)
- ADR-015 (não abstrair por antecipação), ADR-016 (custódia vs responsável), ADR-020, ADR-022
- `conformance/ndf/valid/origem-nao-apuravel.json` e os dois vetores negativos correspondentes
