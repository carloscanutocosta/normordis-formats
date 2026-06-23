# Conformidade RFC 8785 / JCS

`vectors.json` é o contrato estrutural independente da linguagem. As
implementações comparam bytes UTF-8 exatos e o digest SHA-256, não a formatação
textual do JSON. Os casos numéricos IEEE-754 do apêndice B da RFC 8785 estão em
`numbers.json`.

```bash
python3 tools/check_jcs_vectors.py
node tools/check-jcs-vectors.mjs
```

Implementações noutras linguagens DEVEM produzir os mesmos bytes.
