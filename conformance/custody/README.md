# Conformidade da cadeia de custódia

Os ficheiros JSON são vetores independentes da linguagem.
`valid-chain.json` DEVE ser aceite e `invalid-chain.json` DEVE ser rejeitado.
O hash de cada evento cobre os bytes RFC 8785 obtidos depois de remover apenas
`event_hash`.

```bash
python3 tools/check_custody.py conformance/custody/valid-chain.json
! python3 tools/check_custody.py conformance/custody/invalid-chain.json
```
