# ADR-013: Proveniência de sistema produtor (`proveniencia_sistema`)

**Estado**: Aceite
**Data**: 2026-08-13
**Decisores**: carloscanutocosta

---

## Contexto

Uma parte substancial — provavelmente maioritária — dos documentos da
Administração Pública moderna é gerada por sistemas determinísticos, sem
autor humano material: liquidações de impostos, notificações, certidões
automáticas, avisos de cobrança. O NDF não tinha onde registar que sistema e
que versão produziu o conteúdo.

O remendo disponível era `participantes` com `tipo: "sistema"` e
`papel: "sistema_tecnico"` (§2.12.2, ADR-006). É inadequado por uma razão
conceptual: um sistema não *participa* na produção de um documento, **produz**
o documento. `participantes` é um índice de intervenientes com referências
opacas a um registo de identidade externo (§2.12.4) — um sistema não tem
identidade nesse sentido, tem nome, versão e regras de cálculo.

Havia ainda uma confusão latente com `proveniencia_ia`: o bloco de IA existe
porque a intervenção de IA exige registo de revisão humana; um motor de
cálculo determinístico não tem revisão humana a registar, e sujeitá-lo ao
mesmo regime seria absurdo. São regimes distintos que exigem estruturas
distintas.

## Decisão

Introduzir um campo de topo opcional `proveniencia_sistema`, **array**:

```json
"proveniencia_sistema": [
  {
    "sistema": { "nome": "Sistema de Liquidação de IRS",
                 "identificador": "at:sliq-irs",
                 "versao": "2026.4.17" },
    "componente": "motor-calculo",
    "versao_componente": "3.2.0",
    "gerado_em": "2026-07-31T03:14:00Z",
    "regra_ref": { "tipo": "tabela-retencao",
                   "identificador": "at:tabelas-irs-2026",
                   "hash": "sha256:..." }
  }
]
```

Decisões estruturais associadas:

1. **Array, não objeto único.** Um documento pode atravessar uma cadeia de
   produção — motor de cálculo, sistema de validação, sistema de emissão —
   cada um com produtor e versão próprios. Limitar a um objeto obrigaria a
   alteração incompatível no primeiro caso real de *pipeline* multi-sistema.
2. **Ordem cronológica normativa**, por `gerado_em` não decrescente. JCS
   (RFC 8785) preserva a ordem dos arrays, logo a ordem entra no
   `payload_hash`; sem regra, dois produtores com os mesmos factos geram
   documentos com hashes diferentes.
3. **`regra_ref`, `build_ref` e `configuracao_ref` seguem o padrão de
   `intervencao_ia.evidencia_ref`** — `{ tipo, identificador, hash }`, não
   strings soltas. São referências externas não resolvidas pelo NDF, em
   paralelo explícito a `participante_ref` (§2.12.4) e a
   `tipo_classificacao_ref` (§3.2.1).
4. **Remover `sistema_tecnico` de `participantes[].papel`** e o campo
   `participantes[].tipo` (ver ADR-006, nota de superveniência).
5. **Fronteira normativa com a IA**: qualquer componente não determinístico
   pertence a `proveniencia_ia`, sem exceção, mesmo quando embebido num
   *pipeline* automático.

## Alternativas consideradas

### Manter `participantes` com `papel: "sistema_tecnico"`

**Prós**: zero alterações estruturais; já existia.

**Contras**: além do erro conceptual (um sistema não participa), o bloco não
tem onde alojar versão, componente ou referência de regra — que é exatamente a
informação que dá valor ao registo. `participante_ref` é uma string opaca:
`"at:sliq-irs"` não distingue a versão 2026.4.17 da 2025.1.0, e é a versão que
determina como o valor foi calculado. Rejeitado.

### Objeto único em vez de array

**Prós**: mais simples de produzir e de ler; cobre a maioria dos casos reais.

**Contras**: transformar objeto em array mais tarde é alteração incompatível.
O custo de suportar cadeias desde já é uma linha de schema; o custo de o
adiar é uma versão major. Rejeitado.

### Registo completo do *pipeline* (SBOM, log de execução)

**Prós**: reprodutibilidade técnica máxima; auditoria completa.

**Contras**: o NDF-core é canonicalizado, assinado e conservado — por vezes
permanentemente. Embutir SBOM ou *log* de execução significa conservar
indefinidamente informação operacional volumosa, potencialmente sensível, e
que revela superfície de ataque a quem receber o pacote. É o mesmo princípio
já decidido para a IA em ADR-005: proveniência essencial no core, evidência
detalhada fora, ligada por referência. Rejeitado.

## Justificação da decisão

O bloco regista o mínimo para **identificação estável da origem e das regras
aplicadas** — deliberadamente *não* "reprodutibilidade". Com `gerado_em` no
core, e já com `ndf_id` como UUID v4, o documento nunca é reproduzível byte a
byte por reexecução do mesmo motor sobre os mesmos dados. Prometer
reprodutibilidade seria prometer o que o formato não pode entregar; o que
entrega é a capacidade de identificar exatamente que sistema, versão e regra
produziram um resultado, e de ir buscar a evidência detalhada onde ela viva.

A fronteira com a IA (ponto 5) é a decisão com mais consequência prática. Sem
ela, um implementador com um componente de IA dentro de um *pipeline*
classificado como "automático" declara o modelo em `proveniencia_sistema` e
contorna o `revisao_humana.estado` obrigatório de §2.13.3 — que é o mecanismo
com maior peso de garantia do NDF. A regra tem de ser normativa e verificável,
não uma recomendação.

`entidade_produtora` (§2.7.3) mantém-se como titular arquivístico e
`imputacao` (ADR-012) como titular jurídico, independentemente de
`proveniencia_sistema`. O sistema não é autor jurídico de coisa nenhuma.

## Consequências

**Positivas**: documentos gerados automaticamente passam a ter origem técnica
identificável e estável; a cadeia de produção multi-sistema é representável
desde a primeira versão; a fronteira com IA fica normativa em vez de
convencional.

**Negativas / mitigações**: `proveniencia_sistema` fica no NDF-core assinado e
é legível por quem receber o pacote — incluindo o particular notificado —
expondo nomes e versões de sistemas internos. Mitigação: princípio do mínimo
declarado normativamente, e nota informativa a alertar que `build_ref` e
`configuracao_ref` podem ser desadequados em documentos de circulação externa.
Coerente com o limite de âmbito de §1.5.

**Compatibilidade**: aditivo quanto ao campo novo; **incompatível** quanto à
remoção de `sistema_tecnico` e de `participantes[].tipo`. Coberto por ADR-007
— o NDF 1.0.0 está em Draft, sem revisão pública aberta e sem implementação
externa conhecida, pelo que não há compatibilidade retroativa real a
preservar. `ndf_version` mantém-se em `1.0.0`.

## Referências

- SPEC.md §2.14, §2.12, §2.13.4, §9.1, §9.2
- ADR-005-proveniencia-ia.md (nota de superveniência)
- ADR-006-participantes-vs-signatarios.md (nota de superveniência)
- ADR-007-versionamento-estabilizacao.md
- ADR-012-imputacao-juridica.md
