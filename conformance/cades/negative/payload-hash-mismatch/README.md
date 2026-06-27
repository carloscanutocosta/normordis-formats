# negative/payload-hash-mismatch

Esqueleto de fixture CAdES B-LTA.

## Estado

Este diretório foi preparado por `tools/scaffold_cades_fixture.py` e ainda não
contém artefactos criptográficos reais.

## Próximos passos

- adicionar `payload.jcs`;
- adicionar `payload.sha256`;
- adicionar `signature.p7s`;
- preencher `certificates/`, `revocation/`, `timestamps/` e `trust/`;
- substituir o `fixture_state` para indicar material real;
- validar com `tools/check_cades_gate.py`.
