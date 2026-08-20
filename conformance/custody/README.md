# Conformidade da cadeia de custódia

Os ficheiros JSON são vetores independentes da linguagem. O hash de cada evento
cobre os bytes RFC 8785 obtidos depois de remover apenas `event_hash`.

| Vetor | Resultado esperado | O que prova |
|---|---|---|
| `valid-chain.json` | aceite | cadeia encadeada bem formada |
| `invalid-chain.json` | rejeitado | `event_hash` incorrecto |
| `captura-chain.json` | aceite | ciclo completo de um documento capturado: `capturado` → `finalizado` → `verificado` → `eliminado`, com digests de componentes na captura, na verificação de fixidez e na destruição |
| `omissao-recomposta.json` | rejeitado | `CUST-REQ-004` — retirar um evento e **renumerar** a cadeia para dissimular a omissão quebra o encadeamento e é detetável |

`omissao-recomposta.json` é o vetor que dá corpo à propriedade de §2.4.4: uma
transferência parcial de evidência é legítima e visível — saltos de `sequence`
e ligação de hash que não fecha —, mas recompor a cadeia para a fazer passar por
completa não é possível sem quebrar o encadeamento.

```bash
python3 tools/check_custody.py conformance/custody/valid-chain.json
python3 tools/check_custody.py conformance/custody/captura-chain.json
! python3 tools/check_custody.py conformance/custody/invalid-chain.json
! python3 tools/check_custody.py conformance/custody/omissao-recomposta.json
```
