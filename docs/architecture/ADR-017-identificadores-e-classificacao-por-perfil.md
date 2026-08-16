# ADR-017: Identificadores institucionais e classificação de segurança sem vocabulário nacional

**Estado**: Aceite
**Data**: 2026-08-15
**Decisores**: carloscanutocosta

---

## Contexto

ADR-015 retirou do NDF-core o vocabulário arquivístico português, passando-o
para perfis jurisdicionais. Revisão externa de 2026-08-15 observou que a
operação ficou incompleta: dois campos de `metadados` continuavam a codificar
Portugal diretamente no core.

**`entidade_produtora`** admitia `nif`, validado como exatamente nove dígitos, e
`codigo_dglab`. Ambos opcionais, logo não bloqueavam nenhuma jurisdição — mas
uma entidade francesa ou alemã não tinha onde declarar o seu identificador
institucional, e o core continha a sintaxe de um identificador fiscal nacional.

**`classificacao_seguranca`** era um `enum` fechado com os seis níveis do
DL n.º 11/2023, citado como tal na descrição do schema. Aqui o problema é maior
do que o dos identificadores: a classificação de segurança **não é
universalmente representável** por um único vocabulário. O regime da União
Europeia (`RESTREINT UE`, `CONFIDENTIEL UE`, `SECRET UE`, `TRÈS SECRET UE`), os
regimes NATO e os regimes de cada Estado-membro divergem em etiquetas, número
de níveis e regras de manuseamento. É exatamente o padrão de divergência que
levou à generalização de `avaliacao`, e não exigiu levantamento comparativo
para ser reconhecido.

Aplicando o teste de admissão do `ROADMAP.md`: ambos os casos param no portão 4
— são variação jurisdicional de algo que já existe, logo matéria de perfil e
não primitiva nova. E ambos passam a regra do ADR-015: é possível nomear três
sistemas reais que divergem em cada eixo.

## Decisão

1. **`entidade_produtora.nif` e `.codigo_dglab` são substituídos por
   `entidade_produtora.identificadores`** — array de `{ sistema, valor }`, onde
   `sistema` é um identificador opaco qualificado de dois ou mais segmentos
   (`pt-nif`, `pt-dglab`, `fr-siren`, `nl-kvk`, `eu-vat`, `eu-pic`), com o
   mesmo padrão e a mesma justificação de `avaliacao.perfil`.

2. **A validade do `valor` face às regras do esquema não é verificada pelo
   NDF.** O core deixa de conhecer a sintaxe de qualquer identificador
   nacional.

3. **`classificacao_seguranca` passa a objeto `{ perfil, nivel }`.** `perfil`
   nomeia o regime aplicável (`pt`, `eu`, `nato`), enum aberto; `nivel` mantém
   o `enum` fechado de seis valores, agora explicitamente definido como
   **escala ordinal neutra** de sensibilidade e não como as etiquetas legais
   de um regime.

4. **A correspondência entre `nivel` e a etiqueta legal do regime é declarada
   pelo produtor e não é verificada por esta especificação.**

5. Mantém-se o que §1.5 estabelece: o campo é sinal descritivo para o sistema
   de custódia, nunca mecanismo de controlo de acesso.

6. **O nível assumido por omissão é retirado.** A regra anterior — omitir o
   campo equivale a `"uso_interno"` — deixou de ser exprimível ao passar de
   escalar a objeto: não é possível inferir um **regime** a partir do silêncio,
   e um nível sem regime não tem significado determinado. A ausência passa a
   significar *não declarada* (§2.7.4.2). Um custodiante que aplique um nível
   conservador por omissão exerce política própria, legítima por §1.5, mas que
   não é leitura do NDF nem declaração do produtor.

## Alternativas consideradas

### `classificacao_seguranca` como string qualificada (`"pt:reservado"`)

**Prós**: mais compacto; um único campo escalar; trivial de comparar por
igualdade.

**Contras**: delega ao perfil **tudo**, incluindo a noção de nível, e perde a
comparabilidade transversal. Um leitor que não conheça o regime `fr:` não
consegue ordenar dois documentos por sensibilidade — que é a única pergunta com
sentido transversal a jurisdições. É o mesmo erro que se rejeitou em ADR-015 ao
recusar delegar o bloco `avaliacao` inteiro ao perfil: abstrair o vocabulário,
manter a estrutura. Aqui a estrutura é a escala ordinal. Rejeitado.

### Manter o enum nacional e documentar o mapeamento fora do formato

**Prós**: nenhuma alteração incompatível; o enum atual serve Portugal sem falha.

**Contras**: obriga qualquer entidade não portuguesa a declarar o seu documento
numa escala cujas etiquetas são as de outro país, com o risco de a
correspondência ser lida como equivalência jurídica. E deixa a citação do
DL n.º 11/2023 dentro do schema, isto é, dentro do contrato. Rejeitado pela
mesma razão que R11.

### Objeto de identificadores com chaves livres (`{"pt-nif": "..."}`)

**Prós**: mais compacto que o array; acesso direto por esquema.

**Contras**: chaves arbitrárias num objeto tornam o schema incapaz de as
validar como conjunto, impedem `additionalProperties: false` e criam variação
de forma dentro de bytes canonicalizados — dois produtores podem exprimir o
mesmo facto com ordenações distintas de chaves não declaradas. O array de
objetos declarados é verificável e tem forma única. Rejeitado.

### Remover `classificacao_seguranca` do core

**Prós**: eliminaria a questão; a sensibilidade poderia viver no sistema de
custódia.

**Contras**: a sensibilidade do conteúdo é facto documental, determinado na
produção, e é precisamente o tipo de informação que tem de acompanhar o
documento quando ele sai do sistema que o criou. Cai no lado "documental" do
princípio de âmbito de `LACUNAS.md`. Rejeitado.

## Justificação da decisão

As duas alterações completam a operação de ADR-015 no mesmo espírito e com o
mesmo critério, em vez de deixarem o core parcialmente generalizado — o que
seria pior do que não ter generalizado nada, por sugerir neutralidade
jurisdicional onde ela não existe.

O ponto 3 merece nota. Poderia argumentar-se que os seis valores de `nivel` são
já portugueses. Não são: `publico`, `uso_interno`, `reservado`, `confidencial`,
`secreto` e `muito_secreto` são termos comuns, não citações legais, e a escala
que formam é reconhecível em qualquer regime de classificação conhecido. O que
era nacional era a **afirmação** de que esta escala é a do DL n.º 11/2023 —
afirmação que sai do schema e passa a ser função do `perfil` declarado.

O ponto 4 é uma limitação assumida e não uma omissão. Verificar se
`{"perfil": "eu", "nivel": "reservado"}` corresponde corretamente a
`RESTREINT UE` exigiria ao NDF arbitrar equivalências entre regimes de
segurança de Estados soberanos. Não tem competência para isso, e fingir que tem
seria pior do que declarar que não tem.

## Consequências

**Positivas**: fecha o último vestígio de vocabulário nacional obrigatório ou
semi-obrigatório no NDF-core; entidades de qualquer jurisdição declaram os seus
identificadores institucionais sem alteração da especificação; a escala de
sensibilidade continua comparável entre jurisdições.

**Negativas / mitigações**: `classificacao_seguranca` passa de escalar a objeto,
o que torna a leitura marginalmente mais verbosa; mitigado por o campo continuar
opcional e por o nível continuar acessível num único acesso. A correspondência
regime↔nível não é verificável pelo formato — limitação declarada em §2.7.4.1,
e matéria para o gate externo de revisão jurídica.

**Compatibilidade**: **incompatível**. Absorvido em 1.0.0 antes de qualquer
publicação, ao abrigo de ADR-007 e do estado nível 1 — Draft. Migrados 31
`entidade_produtora` e 35 `classificacao_seguranca` em casos de conformidade e
exemplos.

## Referências

- SPEC.md §2.7.1, §2.7.2, §2.7.3, §2.7.4, §2.7.4.1, §1.5
- ADR-015-generalizacao-avaliacao-arquivistica.md — mesmo critério, mesmo padrão de identificador
- `ROADMAP.md` — teste de admissão de novas primitivas (portão 4)
- `docs/profiles/README.md` — matriz de compatibilidade jurisdicional
