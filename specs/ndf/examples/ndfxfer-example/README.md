# Exemplo de conjunto de transferência (`.ndfxfer`)

Duas unidades documentais transferidas da Direção-Geral de Exemplo para o
Arquivo Distrital de Exemplo, com a evidência de custódia de cada uma.

**Estado:** exemplo de desenho. O conjunto de transferência **não é** requisito
de conformidade NDF e não está na SPEC: é o desenho de
[`../../../../docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md`](../../../../docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md),
materializado para poder ser exercitado.

## Composição

| Ficheiro | O que é |
|---|---|
| `transferencia.json` | Declaração de composição, em bytes JCS/RFC 8785 |
| `transferencia-envelope.json` | Selo do transmitente sobre esses bytes |
| `evidencia/<ndf_id>.evidencia.json` | Extrato atestado da cadeia de custódia de cada unidade |
| `unidades/<nome>.ndfpkg` | Um pacote por unidade — **gerado, não versionado** |

**As unidades não estão em Git.** São cópias de
[`../ndfpkg-example`](../ndfpkg-example) e
[`../captura-requerimento`](../captura-requerimento), cujos bytes já estão sob
revisão nos respetivos diretórios; duplicá-los aqui seria ruído. Reconstrua-as
com:

```bash
python3 tools/build_ndfxfer_example.py
python3 tools/check_transferencia.py specs/ndf/examples/ndfxfer-example
```

O construtor recalcula `unidades[]`, `referencias_externas[]`, o inventário e o
selo a partir das unidades reais, pelo que uma alteração a um pacote de exemplo
se propaga sem edição manual de digests.

## O que este exemplo exercita

**Fecho nos dois sentidos.** Cada unidade declarada tem de estar presente, e cada
pacote presente tem de estar declarado — a regra de `NDF-PKG-009` elevada ao
conjunto. Um pacote a mais é tão grave como um a menos: foi acrescentado por
alguém, e o selo não o cobre.

**Ligação à versão exata.** As unidades são identificadas por `ndf_id` **e**
`payload_hash`. O digest do ficheiro `.ndfpkg` **não** é usado: o mesmo documento
materializado noutro ZIP continua a ser a mesma unidade documental (§8.1), e é o
conteúdo que interessa prender, não a embalagem.

**Referências pendentes (D-XFER-1).** O ofício declara `responde_a` o ofício
n.º 45/2026, que não faz parte do conjunto. `referencias_externas[]` declara-o —
e o recetor **recomputa** a lista a partir das unidades que recebeu e compara. É
o que responde à pergunta que o conjunto existe para responder: *este conjunto
fecha sobre si mesmo?*

**Evidência de custódia como extrato atestado (D-XFER-2).** As duas unidades
mostram os dois casos:

| Unidade | Cadeia | Extrato |
|---|---|---|
| Ofício | 2 eventos | integral — `omitidos.contagem` é `0`, e o fundamento declara-o |
| Requerimento | 6 eventos | 4 transferidos, 2 retidos (exportações que identificam trabalhadores do serviço) |

O extrato **não é a cadeia com menos eventos** — seria mutilá-la, o que
`CUST-REQ-004` proíbe e `conformance/custody/omissao-recomposta.json` demonstra
ser detetável. É objeto novo, selado, que declara o que transferiu e o que reteve.
As `sequence` do extrato parcial têm saltos, e é isso que torna a omissão visível
em vez de dissimulada.

**O que o recetor não consegue verificar** está declarado, não escondido:
`eventos_total` e `ultimo_event_hash` são afirmação do transmitente coberta pelo
selo. Um extrato não é uma cadeia completa verificada, e um leitor não deve
tratá-los como equivalentes.

## Vetores negativos

```bash
python3 tools/check_transferencia_vectors.py
```

Onze mutações, cada uma uma família de requisito — unidade ausente, unidade a
mais, `payload_hash` divergente, selo ausente, selo que não cobre, referência
externa omitida, referência externa inventada, contagem de eventos que não fecha,
evento editado, evento fora da política, política sem `finalizado`. Sem elas, «o
conjunto está completo» seria alegação e não propriedade.

## A resposta do recetor

A aceitação é documento próprio, produzido pelo Arquivo Distrital e devolvido ao
transmitente: `conformance/ndf/valid/aceitacao-custodia.json`, do tipo
`aceitacao-custodia@1.0.0`. Exercita aceitação **parcial** — uma unidade aceite,
outra recusada com fundamento —, que é o caso normal e não a exceção.
