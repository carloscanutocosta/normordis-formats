# Vetores de conformidade `.ndfpkg`

Os vetores são produzidos de forma reproduzível a partir do pacote positivo
`specs/ndf/examples/ndfpkg-example`. Cada mutação representa uma família de
requisito e DEVE ser rejeitada.

| ID | Mutação | Requisito principal |
|---|---|---|
| `PKG-NEG-001` | hash de inventário alterado | `NDF-PKG-003`, `NDF-PKG-004` |
| `PKG-NEG-002` | ficheiro não inventariado | autocontenção e inventário fechado |
| `PKG-NEG-003` | nome duplicado no inventário | identidade unívoca dos objetos |
| `PKG-NEG-004` | caminho com `..` | segurança de extração |
| `PKG-NEG-005` | NDT referenciado ausente | `NDF-PKG-006` |
| `PKG-NEG-006` | identidade interna do NDT divergente | resolução NDF ↔ NDT |
| `PKG-NEG-007` | envelope assinado sem timestamps | `NDF-READ-006`, `NDF-READ-008` |

```bash
python3 tools/check_package_vectors.py
```
