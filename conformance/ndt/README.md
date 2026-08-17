# Conformidade NDT

Os exemplos válidos encontram-se em `specs/ndt/examples/` e são executados
como parte da suite NDT. `invalid/` contém casos que DEVEM ser rejeitados.

```bash
python3 tools/validate.py --format ndt
```

Todos os requisitos de produtor NDT são verificáveis sobre um único ficheiro:
cada `versao_ndt` é um template autónomo e não existem requisitos de
compatibilidade entre versões (SPEC §8.2).
