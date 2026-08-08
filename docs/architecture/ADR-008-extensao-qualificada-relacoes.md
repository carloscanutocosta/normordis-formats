# ADR-008: Extensão qualificada do vocabulário de `relacoes[].tipo`

**Estado**: Aceite
**Data**: 2026-08-08
**Decisores**: carloscanutocosta

---

## Contexto

`relacoes[].tipo` (ADR-002) usa um enum fechado de 11 valores. `LACUNAS.md`
L4 identificou que este vocabulário, ao contrário de `tipo_documento_ref`
(registo extensível por entidade, `specs/registry/`), só se estende por
nova versão minor desta especificação. Isto é uma inconsistência de
arquitetura: um município ou a AT podem ter necessidade legítima de um tipo
de relação específico do seu domínio (ex.: "retificação oficiosa"), sem que
isso justifique pedir uma alteração à especificação base NDF.

## Decisão

`relacoes[].tipo` passa a aceitar, além do vocabulário base fechado, um
valor de **extensão qualificada** no formato `ext.<entidade>.<tipo>` (ex.:
`ext.at.retificacao-oficiosa`). Implementado com `oneOf` no JSON Schema:
um ramo é o enum de 11 valores (inalterado), o outro é um padrão de string
qualificada. Sem registo central — o namespace `<entidade>` é autodeclarado.

## Alternativas consideradas

### Manter o enum totalmente fechado, extensão só por versão minor

**Prós**: vocabulário sempre coerente e revisto centralmente; zero risco de
colisão semântica entre entidades.

**Contras**: é exatamente a rigidez que o `LACUNAS.md` L4 identificou como
problema — força qualquer necessidade legítima de uma entidade a passar por
um processo de alteração da especificação base, com o atrito e a demora
que isso implica, para uma necessidade que é, por natureza, local a essa
entidade. Rejeitado.

### Enum totalmente aberto (qualquer string)

**Prós**: máxima flexibilidade, implementação trivial.

**Contras**: perde-se toda a disciplina de vocabulário controlado que o
resto da especificação usa consistentemente (`classificacao_seguranca`,
`destino_final`, `nivel_assinatura`). Um leitor deixaria de conseguir
distinguir "isto é uma relação do vocabulário normativo NDF" de "isto é uma
convenção interna de um produtor específico" — perda de interoperabilidade
sem ganho correspondente. Rejeitado.

### Registo central de extensões (como `specs/registry/` para tipos de documento)

**Prós**: manteria descoberta e alguma governação sobre extensões, evitando
colisões semânticas reais.

**Contras**: peso desproporcional para o problema — criar um segundo
mecanismo de registo (além do já existente para tipos de documento) só
para tipos de relação, sem evidência de que a procura justifica esse
investimento agora. Pode ser reconsiderado no futuro se surgir necessidade
real de descoberta cruzada de extensões entre entidades; nesta versão, o
autodeclarado é suficiente e consistente com o princípio geral desta
especificação de minimizar infraestrutura central.

## Justificação da decisão

O formato `ext.<entidade>.<tipo>` segue uma convenção já bem estabelecida
noutros ecossistemas para extensibilidade sem coordenação central
(namespaces XML, pacotes Java, propriedades customizadas em vCard/iCal) —
resolve colisão por convenção social (a entidade usa o seu próprio
identificador organizacional como prefixo), não por imposição técnica.
`oneOf` no JSON Schema garante que um valor não pode simultaneamente
pertencer ao vocabulário base e ao formato de extensão — mantém a distinção
nítida entre os dois.

Um leitor que não reconheça uma extensão qualificada **NÃO DEVE** rejeitar
o documento só por isso — a relação continua estruturalmente válida
(`alvo.ndf_id` + `alvo.payload_hash` verificáveis); só a interpretação
semântica fica limitada. Isto preserva a verificabilidade criptográfica da
relação mesmo quando o significado exato da extensão é desconhecido ao
leitor.

## Consequências

**Positivas**: entidades podem modelar relações específicas do seu domínio
sem esperar por uma versão da especificação base; a relação continua
verificável por hash independentemente de o `tipo` ser reconhecido.

**Negativas / mitigações**: risco de colisão semântica entre extensões
autodeclaradas de entidades diferentes com o mesmo `<entidade>` —
mitigado por `<entidade>` corresponder tipicamente a um identificador
organizacional já reconhecido (código DGLAB, sigla). Sem registo central,
não há descoberta automática do significado de uma extensão — aceite como
compromisso proporcional ao problema (ver alternativas rejeitadas).

**Compatibilidade**: aditivo — todos os 11 valores do vocabulário base
continuam válidos; nenhum documento produzido antes desta alteração deixa
de validar.

## Referências

- SPEC.md §2.11.2, §2.11.7
- ADR-002-relacoes-no-core.md
- `LACUNAS.md` L4
