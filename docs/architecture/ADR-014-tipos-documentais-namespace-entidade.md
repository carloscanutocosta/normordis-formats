# ADR-014: Tipos documentais por namespace de entidade

**Estado**: Aceite
**Data**: 2026-08-13
**Decisores**: carloscanutocosta

---

## Contexto

`metadados.tipo_documento_ref` (§2.9.2) referencia um schema do registo
canónico em `specs/registry/schemas/`. O registo tem hoje cinco tipos:
`oficio`, `despacho`, `informacao-tecnica`, `parecer`, `modelo3-irs`.

Ao modelar o primeiro caso de documento gerado automaticamente — a liquidação
de IRS — tornou-se evidente que a estratégia não escala. Uma liquidação de IRS
exigiria `liquidacao-irs`; a seguir `liquidacao-iva`, `liquidacao-imi`,
`liquidacao-iuc`, `liquidacao-is`; depois as notificações correspondentes; e
isso apenas para a AT. Multiplicando pelos organismos da AP com tipologia
documental própria — segurança social, municípios, conservatórias,
universidades — o registo canónico atinge um número indeterminado de tipos que
o NORMORDIS não tem capacidade nem legitimidade para manter. Um registo que
não é mantido deixa de ser fonte de verdade e passa a ser ruído.

Há um segundo problema, independente e pré-existente. Em
`check_ndf_semantic`, o schema do tipo é resolvido em
`specs/registry/schemas/<tipo_id>.schema.json` e, **quando não existe, a
validação de `documento` é simplesmente saltada** — o caso passa sem qualquer
verificação. Um `tipo_documento_ref` inexistente é hoje indistinguível de um
tipo válido, o que é um falso positivo silencioso.

Existe ainda uma inconsistência de arquitetura: `relacoes[].tipo` já resolveu
exatamente este problema em ADR-008, com o formato `ext.<entidade>.<tipo>`.
O eixo dos tipos documentais ficou sem o mecanismo equivalente.

## Decisão

1. `metadados.tipo_documento_ref` passa a aceitar, além do formato canónico
   `<id>@<versao>`, um formato de **extensão qualificada**:
   `ext.<entidade>.<tipo>@<versao>` — por exemplo
   `ext.at.liquidacao-irs@2026.1`. Mesmo mecanismo, mesmo regime de
   responsabilidade e mesma justificação de ADR-008: namespace autodeclarado,
   semântica definida pela entidade que o declara.
2. O registo canónico fica reservado a **formas documentais transversais** —
   as que atravessam organismos e cuja estrutura é matéria de normalização
   (ofício, despacho, informação, parecer). Tipos de domínio vivem no
   namespace da entidade que os define e mantém.
3. O schema do tipo **viaja dentro do `.ndfpkg`**, em `schemas/`. Já
   acontecia na prática (`ndfpkg-example/schemas/oficio.schema.json`), sem
   estar declarado como mecanismo.
4. Corrigir a resolução de schema: passa a resolver **preferencialmente a
   partir do pacote**, com recurso ao registo canónico apenas fora do contexto
   de pacote.
5. Fechar o falso positivo silencioso: tipo canónico não resolvido é **erro**;
   tipo `ext.*` não resolvido em contexto de pacote é **erro** (tem de vir no
   pacote); em ficheiro solto é **advisory**, por não haver onde o resolver.

## Alternativas consideradas

### Um tipo genérico parametrizado (`liquidacao@1.0.0` com campo `tributo`)

**Prós**: um só tipo no registo cobre todas as liquidações; evita a explosão
sem introduzir mecanismo novo.

**Contras**: as liquidações partilham a forma mas não a estrutura — a
demonstração de liquidação de IRS não tem os mesmos campos que a de IMI, e um
schema que acomode ambas tem de ser permissivo ao ponto de não validar nada de
útil. E empurra o problema em vez de o resolver: a seguir às liquidações vêm as
notificações, as certidões, os autos. Rejeitado por trocar explosão de tipos
por erosão da validação.

### Manter tudo no registo canónico

**Prós**: descoberta centralizada; um só sítio para procurar qualquer tipo.

**Contras**: é o problema descrito no contexto. Exigiria também que cada
entidade submetesse os seus tipos a um processo de alteração do registo
NORMORDIS, com o atrito correspondente, para tipos que são por natureza locais
a essa entidade e sobre os quais o NORMORDIS não tem competência material.
Rejeitado.

### Permitir qualquer `tipo_documento_ref`, sem validação de `documento`

**Prós**: flexibilidade total; é aproximadamente o comportamento atual.

**Contras**: é precisamente o falso positivo silencioso que esta decisão
existe para fechar. `documento` deixaria de ter garantia estrutural nenhuma, e
`NDF-PROD-001` tornar-se-ia uma afirmação vazia para qualquer tipo não
registado. Rejeitado.

## Justificação da decisão

A decisão transporta para os tipos documentais o raciocínio já aceite em
ADR-008 para as relações, o que reduz o número de mecanismos distintos na
especificação em vez de o aumentar: uma única convenção `ext.<entidade>.*`
para extensibilidade sem coordenação central, aplicada a dois eixos.

O ponto 3 é o que torna a decisão segura. Num registo central, um tipo
desconhecido é irrecuperável para um terceiro. Dentro de um `.ndfpkg`, o
schema acompanha o documento: um verificador independente — em qualquer
linguagem — valida `documento` contra o schema que veio no pacote, sem acesso
a registo nenhum. Isto reforça a garantia de autocontenção de §8.3 em vez de a
enfraquecer, e é o que permite abrir o namespace sem perder a validação.

A assimetria com ADR-008 é intencional e vale a pena explicitá-la: uma relação
de tipo desconhecido **não deve** levar à rejeição do documento, porque
continua verificável por hash e só a interpretação semântica fica limitada. Um
`documento` cujo schema não é resolúvel **é** motivo de rejeição em contexto de
pacote, porque sem schema não há qualquer garantia estrutural sobre o conteúdo.
Tolerância semântica num caso, exigência estrutural no outro.

## Consequências

**Positivas**: o registo canónico mantém-se pequeno e mantível; entidades
modelam a sua tipologia sem esperar por versão da especificação; fecha-se um
falso positivo silencioso pré-existente; o `.ndfpkg` torna-se genuinamente
autocontido para efeitos de validação de `documento`.

**Negativas / mitigações**: sem registo central de extensões não há descoberta
automática do significado de um tipo `ext.*` — mesmo compromisso já aceite em
ADR-008, e mitigado por o schema viajar no pacote (a estrutura é sempre
descobrível, mesmo quando a semântica não é). Risco de colisão de namespace,
mitigado por `<entidade>` corresponder tipicamente a identificador
organizacional já reconhecido.

**Compatibilidade**: aditivo quanto ao formato de referência — todos os
`tipo_documento_ref` canónicos continuam válidos. A correção do ponto 5 é
**mais estrita** do que o comportamento atual: um NDF com tipo não resolúvel
que hoje passa, passa a ser rejeitado. Coberto por ADR-007.

## Referências

- SPEC.md §2.9.2, §8.1, §9.1, §9.3
- ADR-008-extensao-qualificada-relacoes.md
- ADR-003-documentos-autonomos.md
- `tools/validate.py` — `check_ndf_semantic`, `validate_package_dir`
