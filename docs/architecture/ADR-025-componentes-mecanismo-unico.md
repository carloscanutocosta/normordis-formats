# ADR-025: `componentes` é o mecanismo único de binários, também na via nativa

**Estado**: Aceite
**Data**: 2026-08-23
**Decisores**: carloscanutocosta

---

## Contexto

[ADR-020](ADR-020-um-formato-duas-realidades.md) separou duas realidades — o
documento nativo, cujo conteúdo vive em campos estruturados, e o documento
capturado, cujo conteúdo vive em componentes binários. A separação está certa e
não é o que este ADR revê.

O que ficou por decidir é o caso que atravessa as duas: **um documento nativo
com anexos que não são nativos.** Um ofício com um mapa de medições, uma
informação técnica com uma planta, um parecer com o extrato que o fundamenta. É
o caso corrente da administração, não a exceção.

O NDF respondia-lhe com um **segundo vocabulário**. `oficio.schema.json` e
`informacao-tecnica.schema.json` declaravam `anexos[]` — `descricao`,
`hash_sha256`, `nome_ficheiro` — enquanto `documento-capturado` declarava
`componentes[]` — `id`, `papel`, `media_type`, `sha256`, `tamanho`,
`nome_original`, `validacao_formato`, `derivado_de`.

Dois vocabulários para binários significam duas regras de fecho de pacote, e só
uma estava verificada. `NDF-PKG-009` fecha sobre «cada componente declarado em
`documento` nos termos de §2.8.1» — que é `componentes[]` e não `anexos[]`.

### O efeito, verificado antes desta decisão

| Situação | Resultado |
|---|---|
| Ofício declara anexo **e transporta-o** em `anexos/` | **rejeitado** — «ficheiro em `anexos/` não corresponde a nenhum componente declarado» |
| Ofício declara anexo **e não o transporta** | **aceite** |

O formato empurrava o produtor para o pacote incompleto: a única via conforme
era não enviar o anexo. E contradizia o seu próprio texto, porque §8.1 já
afirmava que «não há categoria de componente documental omissível» — havia uma,
e era a mais comum.

O `anexos[]` do ofício não era usado por nenhum NDT, exemplo ou vetor: era
vocabulário declarado e nunca exercitado, o que explica por que a incoerência
sobreviveu.

## Decisão

**`componentes` é o mecanismo único de componentes binários no NDF. Qualquer
schema de tipo PODE declará-lo; nenhum DEVE definir vocabulário próprio para o
mesmo fim.** `anexos[]` é retirado dos dois tipos que o tinham.

Um anexo de documento nativo é um componente com `papel: "anexo"` (SPEC
§2.8.1.3). Daqui decorrem, sem regra nova:

- o digest do anexo entra nos `payload_bytes` e fica coberto pela assinatura
  ([ADR-021](ADR-021-componentes-nos-bytes-assinados.md));
- o anexo viaja no `.ndfpkg`, em `anexos/`;
- `NDF-PKG-009` fecha nos dois sentidos também para a via nativa.

### O teste de identidade documental

A fronteira entre as duas formas de anexar não é o formato do ficheiro, é o que
o anexo **é**:

> O anexo tem existência documental própria — autor, data, número, ciclo de
> vida, avaliação ou autenticidade que não sejam os do documento que acompanha?

**Não** → `componentes[]` com `papel: "anexo"`, dentro deste NDF.
**Sim** → NDF autónomo, ligado por `relacoes[{ tipo: "anexa" }]`.

O segundo caso não contorna o primeiro: é o que permite ao anexo ter avaliação
arquivística, prazo de conservação, assinatura e destino final próprios, e
continuar identificável quando o documento que acompanhava for eliminado.

## Alternativas consideradas

### Alargar `NDF-PKG-009` para reconhecer também `anexos[]`

Resolveria o sintoma imediato — o ofício passaria a transportar o anexo — e
consolidaria a causa. O fecho de pacote passaria a conhecer dois vocabulários, e
cada tipo novo poderia inventar um terceiro. Um verificador teria de os conhecer
a todos para decidir conformidade, o que é o oposto de um contrato verificável.

### Manter `anexos[]` como forma «leve», e `componentes[]` como forma «completa»

Tem apelo: `descricao` + `hash` é mais barato de preencher do que sete campos.
Mas os campos em falta não são acessórios — sem `media_type` um leitor não sabe
como abrir o anexo, sem `tamanho` não sabe o que vai receber, e sem `id` nada o
pode referenciar. E a forma leve seria a mais usada, por ser a mais fácil, com o
resultado de a maioria dos anexos ficar sem a informação que os torna
utilizáveis a longo prazo.

### Tratar todo o documento com anexos como `documento-capturado`

Obrigaria a abandonar a estrutura do ato para poder anexar um ficheiro, isto é,
a perder a via nativa exatamente no caso em que ela é mais útil: um ofício
continua a ser um ofício por ter um mapa em anexo.

## Justificação da decisão

É a aplicação direta de [ADR-022](ADR-022-dever-do-formato.md): o dever do
formato é que **toda a informação relevante e necessária tenha onde ser
guardada**. «Este ofício leva este anexo, com este conteúdo exato» é informação
relevante, era necessária, e não tinha onde ser guardada de forma que o pacote
transportasse — logo, lacuna do formato.

O critério de admissão de novas primitivas (`ROADMAP.md`) não é sequer
convocado, porque **não há primitiva nova**: `componentes` já existia, já estava
especificado em §2.8.1 como faculdade de qualquer schema de tipo, e já tinha
fecho de pacote verificado. O que existia era um tipo a não a usar.

## Consequências

**Positivas**: o caso mais comum da administração — ato próprio com anexo de
terceiro — passa a ser representável e transportável sem tipo especial e sem
sair da via nativa. Um vocabulário único significa uma regra de fecho, um
conjunto de vetores e um verificador que não precisa de tabela de equivalências.

**Negativas / mitigações**: **incompatível** para quem tivesse usado `anexos[]`
— absorvido em 1.0.0 antes de publicação, ao abrigo de ADR-007 e do estado
nível 1 — Draft, e sem instâncias a migrar, por o campo nunca ter sido
exercitado. Preencher um componente exige mais do que preencher a entrada
anterior; é o custo de o anexo ser utilizável por quem o receber daqui a dez
anos.

A definição fica **duplicada** entre schemas de tipo, porque um schema de tipo é
autocontido por desenho — um pacote transporta um e tem de o validar sem rede, e
não há `$ref` entre ficheiros em parte nenhuma do projeto. Duplicação sem guarda
deriva, que foi como esta incoerência nasceu; a mitigação é a verificação **C7**
em `tools/check_spec_coherence.py`, que rejeita tanto `componentes.items`
divergente como o reaparecimento de um vocabulário paralelo.

## Referências

- SPEC.md §2.8.1, §2.8.1.3 (anexos de documento nativo), §8.1, `NDF-PKG-009`
- ADR-020, ADR-021, [ADR-022](ADR-022-dever-do-formato.md), ADR-007
- `conformance/package/README.md` — `PKG-NEG-015`, `PKG-NEG-016`
- `specs/ndf/examples/ndfpkg-example/` — ofício com anexo, exemplo de referência
