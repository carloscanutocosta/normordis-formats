# Conformidade da cadeia de custódia

Os ficheiros JSON são vetores independentes da linguagem. O hash de cada evento
cobre os bytes RFC 8785 obtidos depois de remover apenas `event_hash`.

| Vetor | Resultado esperado | O que prova |
|---|---|---|
| `valid-chain.json` | aceite | cadeia encadeada bem formada |
| `invalid-chain.json` | rejeitado | `event_hash` incorrecto |
| `captura-chain.json` | aceite | ciclo completo de um documento capturado: `capturado` → `finalizado` → `verificado` → `eliminado`, com digests de componentes na captura, na verificação de fixidez e na destruição |
| `omissao-recomposta.json` | rejeitado | `CUST-REQ-004` — retirar um evento e **renumerar** a cadeia para dissimular a omissão quebra o encadeamento e é detetável |
| `cadeia-do-recetor.json` | aceite | cadeia do **custodiante recetor** para um documento recebido de outra entidade: abre em `recebido`, `sequence` 0, `previous_event_hash` `null`. As cadeias são por custodiante e não continuam a do transmitente (§2.4.2) |

`omissao-recomposta.json` é o vetor que dá corpo à propriedade de §2.4.4: uma
transferência parcial de evidência é legítima e visível — saltos de `sequence`
e ligação de hash que não fecha —, mas recompor a cadeia para a fazer passar por
completa não é possível sem quebrar o encadeamento.

`cadeia-do-recetor.json` exercita a propriedade que decorre daí: se as cadeias
fossem globais, o recetor teria de continuar a do transmitente — e não pode, por
não deter os eventos anteriores nem os poder encadear sem os falsificar. A
ligação entre custodiantes é documental (evidência transferida + documento de
aceitação), nunca criptográfica.

```bash
python3 tools/check_custody.py conformance/custody/valid-chain.json
python3 tools/check_custody.py conformance/custody/captura-chain.json
python3 tools/check_custody.py conformance/custody/cadeia-do-recetor.json
! python3 tools/check_custody.py conformance/custody/invalid-chain.json
! python3 tools/check_custody.py conformance/custody/omissao-recomposta.json
```
