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
| `PKG-NEG-008` | assinatura sem `assinatura_id` | §4.4.1 |
| `PKG-NEG-009` | NDT com referência de campo pendurada | `check_ndt_bindings`, ADR-independente |
| `PKG-NEG-015` | anexo de documento **nativo** declarado e ausente do pacote | `NDF-PKG-009`, §2.8.1.3 |
| `PKG-NEG-016` | ficheiro em `anexos/` inventariado e não declarado | `NDF-PKG-009`, sentido inverso |
| `PKG-NEG-017` | texto fixo do NDT alterado, só o hash físico do manifesto recalculado | `NDF-PKG-010`, `NDF-READ-025` |
| `PKG-NEG-018` | schema do perfil (`pt-dglab`) trocado mantendo o identificador, só o manifesto recalculado | `NDF-PKG-010`, `NDF-READ-025` |
| `PKG-NEG-019` | entrada `schema_perfil` omitida de `dependencias_interpretacao` | `NDF-PROD-025` |
| `PKG-NEG-020` | schema de tipo **canónico** (`oficio`, não extensão) trocado mantendo o identificador, só o manifesto recalculado | `NDF-PKG-007`, `NDF-PKG-010`, `NDF-READ-025` |
| `PKG-NEG-021` | recurso do NDT (`recursos/`) trocado mantendo o nome, só o manifesto recalculado | `NDF-PKG-011`, `NDF-READ-026` |

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

`PKG-NEG-017` reproduz, ponto por ponto, o achado de uma revisão adversarial
assistida por IA (2026-09-11, `docs/reports/READINESS-ASSESSMENT.md` R16):
antes de `dependencias_interpretacao` (ADR-026), o hash do NDT só existia em
`manifest.json`, fora dos bytes assinados — alterar o template e recalcular
só o manifesto passava. `PKG-NEG-018` é o mesmo ataque aplicado ao schema do
perfil de avaliação.

`PKG-NEG-020` e `PKG-NEG-021` fecham duas lacunas encontradas por revisão
adversarial à *primeira* implementação de `dependencias_interpretacao`
(commit `3985001`): schemas de tipo **canónico** (não só extensão
qualificada, R24) e recursos do NDT referenciados por hash (R23) ficaram,
nessa primeira ronda, sem a mesma proteção do NDT.

```bash
python3 tools/check_package_vectors.py
```
