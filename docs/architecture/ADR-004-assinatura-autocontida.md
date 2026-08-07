# ADR-004: Material de validação por assinatura (unidade de prova autocontida)

**Estado**: Aceite
**Data**: 2026-08-07
**Decisores**: carloscanutocosta

---

## Contexto

O envelope NDF sempre suportou múltiplas assinaturas (`assinaturas[]` é um
array desde a versão inicial). Contudo, `timestamps` e `validation_material`
eram campos de **topo do envelope**, partilhados por todas as entradas de
`assinaturas[]`. Com uma única assinatura isto é inofensivo; com mais do que
uma — cada uma potencialmente com certificado, cadeia de confiança, dados de
revogação (OCSP/CRL) e instante de assinatura distintos — a estrutura torna-
se ambígua: não é possível determinar, a partir do envelope, que par de
timestamp/material de validação corresponde a qual assinatura.

## Decisão

Mover `timestamps` e `validation_material` para dentro de cada entrada de
`assinaturas[]`. Cada assinatura passa a ser uma **unidade de prova
autocontida**: identidade, certificado, timestamps RFC 3161 e material de
validação próprios, mais um `assinatura_id` estável e, opcionalmente,
`papel` e `ordem`.

## Alternativas consideradas

### Modelo dual — campos globais quando há uma assinatura, por assinatura quando há mais do que uma

**Prós**: preservaria a forma exata dos envelopes de assinatura única já
existentes.

**Contras**: cria dois caminhos de leitura válidos para o mesmo dado; um
verificador teria de saber qual usar em cada caso, sem ganho real de
compatibilidade — não existe, à data desta decisão, nenhuma implementação
nem consumidor externo do formato de envelope anterior (confirmado
explicitamente antes de decidir), pelo que não há nada de real a proteger
com um modelo dual.

### Manter campos globais e acrescentar apenas um índice de qual assinatura "é a principal"

**Prós**: menor alteração de estrutura.

**Contras**: não resolve o problema de fundo — continuaria a existir apenas
um `timestamps`/`validation_material` para N assinaturas potencialmente
distintas; um índice não substitui dados que precisam de existir N vezes.

## Justificação da decisão

CAdES-B-LTA (ETSI EN 319 122) já trata cada assinatura como uma prova
independente, com o seu próprio timestamp de arquivo sobre a própria
assinatura mais o seu próprio material de validação — o envelope NDF estava,
antes desta decisão, a agregar artificialmente algo que o próprio padrão
CAdES trata como local a cada assinatura. Corrigir isto alinha o NDF com o
modelo que já usa.

## Consequências

**Positivas**: nenhuma ambiguidade possível entre N assinaturas
independentes; cada assinatura pode ser adicionada, verificada ou destacada
sem depender de estado partilhado.

**Negativas / mitigações**: forma do envelope de assinatura única muda
face à versão anterior — sem impacto real por não existir adoção externa
(confirmado); o exemplo `.ndfpkg` existente (`specs/ndf/examples/ndfpkg-example/`)
e o validador de referência (`tools/validate.py`) foram atualizados no mesmo
lote de alterações desta ADR.

## Referências

- SPEC.md §4.4, §4.4.1
- `specs/ndf/schemas/envelope.schema.json`
- ETSI EN 319 122 (CAdES)
