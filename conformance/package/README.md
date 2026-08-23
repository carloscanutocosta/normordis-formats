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
| `PKG-NEG-015` | anexo de documento **nativo** declarado e ausente do pacote | `NDF-PKG-009`, §2.8.1.3 |
| `PKG-NEG-016` | ficheiro em `anexos/` inventariado e não declarado | `NDF-PKG-009`, sentido inverso |

Os vetores seguintes derivam do pacote de captura
`specs/ndf/examples/captura-requerimento` e exercitam §2.8.1.

| ID | Mutação | Requisito principal |
|---|---|---|
| `PKG-NEG-010` | componente declarado ausente do pacote e do inventário | `NDF-PKG-009` |
| `PKG-NEG-011` | bytes do componente alterados e inventário atualizado, NDF-core não | `NDF-PKG-009` |
| `PKG-NEG-012` | ficheiro em `original/` inventariado mas não declarado como componente | `NDF-PKG-009`, sentido inverso |
| `PKG-NEG-013` | original reescrito e NDF-core «harmonizado» com os novos bytes | `NDF-PROD-020` |
| `PKG-NEG-014` | documento capturado sem estado de reconstituição | schema do tipo; ADR-022 |

`PKG-NEG-015` e `PKG-NEG-016` existem porque o fecho de `NDF-PKG-009` valia
apenas para a via capturada: o schema do ofício declarava anexos num vocabulário
próprio (`anexos[]`), que o fecho não reconhecia. Um ofício que transportasse o
seu anexo era rejeitado, e um que o omitisse era aceite — o formato empurrava
para o pacote incompleto. Resolvido em §2.8.1.3, com a guarda C7 de
`tools/check_spec_coherence.py` a impedir que um tipo volte a inventar
vocabulário paralelo.

`PKG-NEG-011` é o caso que motiva a colocação dos componentes nos bytes
assinados: sem `NDF-PKG-009`, o pacote passaria — a assinatura cobre o
NDF-core e o manifesto não é assinado.

```bash
python3 tools/check_package_vectors.py
```
