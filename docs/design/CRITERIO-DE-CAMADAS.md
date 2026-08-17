# Critério de colocação por camada

**Estado:** documento de desenho, não normativo. Quando aprovado, o essencial
das cláusulas 2 a 5 destina-se a ser vertido para
[`docs/architecture/ARCHITECTURE.md`](../architecture/ARCHITECTURE.md), que já
fixa o princípio de que PDF, ODF e HTML são projeções do documento lógico.

**Origem:** pedido do responsável do projeto (2026-08-17) — estabelecer o melhor
critério para que os formatos exprimam qualquer documento administrativo ou
legal de forma duradoura e imutável, cumprindo os requisitos aplicáveis, e ao
mesmo tempo permitam alterações de forma ágil.

---

## 1. A tensão aparente

"Imutável" e "alterável de forma ágil" parecem contradizer-se. Não se
contradizem, porque não é a mesma coisa que muda.

Um documento administrativo tem partes que **nunca podem mudar** sob pena de
perder valor probatório, e partes que **têm de poder mudar** sem que isso afete
o valor probatório do que já foi produzido. Confundi-las é o erro que gera
sistemas em que corrigir uma margem obriga a reassinar dez mil documentos, ou —
pior — sistemas em que alterar o texto de um ato é tecnicamente possível.

O critério que se segue resolve isto com uma pergunta única: **quando isto mudar,
o que tem de ser refeito?**

## 2. As camadas e as suas velocidades

Cada camada tem uma velocidade de mudança própria. Uma coisa deve viver na
camada cuja velocidade lhe corresponde.

| Camada | Contém | Muda quando | Mecanismo de mudança | Custo |
|---|---|---|---|---|
| **Custódia** (opcional) | eventos de ingestão, acesso, transição, eliminação | continuamente | novo evento append-only | nulo — é o seu propósito |
| **Envelope** | hash, `validation_code`, assinaturas, timestamps | nunca, salvo re-selagem | re-selagem preservando o original | alto |
| **NDF-core** | dados, metadados, conteúdo NCRTF | **nunca** | novo NDF + `relacoes[substitui]` | muito alto: nova canonicalização, assinatura e custódia |
| **Schema do tipo** | que campos tem um "ofício" | alteração legal ou orgânica | nova versão do tipo no registo | médio: afeta produtores |
| **NDT** | estrutura de página, estilos, geometria | decisão editorial ou de imagem institucional | nova `versao_ndt` | **baixo — e é esse o ponto** |
| **Especificação** | vocabulário dos formatos | evolução do próprio formato | SemVer MINOR/MAJOR | alto: afeta todo o ecossistema |

A leitura decisiva é a comparação entre as linhas do NDF-core e do NDT. São as
duas camadas que descrevem o mesmo documento, e têm custos de mudança separados
por várias ordens de grandeza. **Tudo o que possa razoavelmente mudar ao longo do
tempo sem que o ato mude deve estar do lado do NDT.**

## 3. O teste de colocação

> **Quando isto mudar, é preciso reassinar o documento?**
>
> Se sim, e a mudança **não** é uma mudança do ato — está na camada errada.

Exemplo concreto. Em 2030 decide-se mudar a tipografia da publicação oficial.

- Se a família tipográfica estiver no NCRTF, dentro do `payload_bytes` assinado:
  cada diploma publicado tem de ser reproduzido, recanonicalizado, reassinado e
  registado em custódia — para uma alteração que não muda uma vírgula do texto
  normativo. Absurdo, e juridicamente perigoso: reabre documentos fechados.
- Se estiver no NDT: publica-se uma nova `versao_ndt`, que passa a ser usada
  pelos documentos **futuros**. Nenhum documento existente é tocado — nem
  precisa de ser.

O teste dá a resposta sem discussão. E identifica um problema existente:
`font_family`, `alignment` e `indent` estão hoje no NCRTF, portanto do lado
errado (ver `ODF-ALIGNMENT-STUDY.md` §7.1).

### 3.1 O que a separação garante — e o que não promete

O par NDF+NDT é **fixo**. O `ndt_version_ref` vive dentro do `payload_bytes`
assinado, o `.ndfpkg` incorpora essa versão exata do NDT (`NDF-PKG-006`) e o
renderizador confirma `schema_id@versao_ndt == ndt_version_ref` antes de
renderizar (SPEC NDT §7, passo 4). Um documento está ligado ao template que
declara, para sempre.

Logo, o ganho da separação **não** é poder re-renderizar documentos antigos com
o aspeto novo. É outro, e é maior:

1. **A decisão não se repete em cada instância.** A apresentação é declarada uma
   vez, no template, e não copiada para dentro de cada documento produzido.
2. **Muda-se num sítio só, para o futuro.** Alterar o template altera todos os
   documentos que vierem a ser produzidos com ele — sem alterar o formato, a
   aplicação, ou qualquer documento existente.
3. **Fidelidade histórica por construção.** Um diploma de 2026 renderiza-se
   sempre como foi publicado em 2026, porque transporta o seu template. Isto não
   é um efeito lateral: é um requisito de prova.

Se a apresentação estivesse no conteúdo, perdiam-se os pontos 1 e 2 — cada
documento traria a sua cópia da decisão, sem sítio central onde a mudar, nem
sequer para os futuros. O ponto 3 manter-se-ia, mas ao preço de tornar
imutável aquilo que não precisa de o ser.

**Renderização conforme e derivação.** Aplicar a um NDF um NDT diferente do que
ele declara é tecnicamente possível e por vezes útil — uma versão em corpo
grande para acessibilidade, uma consolidação editorial. Mas não é uma
renderização conforme daquele documento: falha o passo 4 do fluxo de §7. É uma
**derivação**, e não deve ser apresentada como representação fiel do documento
nem servir de base a prova. A distinção merece ficar explícita na SPEC.

## 4. Hierarquia de decisão

Para qualquer elemento novo, por esta ordem. A primeira resposta afirmativa
determina a camada.

1. **É um facto sobre o documento** — quem o produziu, quando, que tipo é, com
   que autoridade, que dados pessoais contém, que destino arquivístico tem?
   → **NDF-core, `metadados` e blocos próprios.**
2. **É o conteúdo que o documento comunica** — os valores, o texto do ato?
   → **NDF-core, `documento`** (e NCRTF, se for texto estruturado).
3. **É a estrutura semântica desse texto** — isto é uma citação legal, isto é
   uma nota de rodapé, isto é o nível 3 de uma enumeração?
   → **NCRTF.**
4. **É a apresentação** — que tipo de letra, que margens, onde na página, que
   numeração se usa no nível 3?
   → **NDT.**
5. **É prova de integridade, autenticidade ou histórico de guarda?**
   → **Envelope ou registo de custódia.**
6. **É estado de um procedimento, regra de negócio, ou decisão sobre quem age a
   seguir?** → **Fora dos formatos.** Pertence ao sistema de gestão documental,
   que referencia o NDF por `ndf_id`/`payload_hash`.

A fronteira entre 3 e 4 é a que mais custa a manter, e resume-se a uma frase:

> **O conteúdo declara o que a coisa É. O template declara como se VÊ.**

Um bloco declara-se `citacao-legal` (papel semântico, estável, parte do ato); o
template declara que uma citação legal se apresenta recuada, a itálico, num
corpo menor (apresentação, alterável).

## 5. As duas formas de alterar

"Alterações ágeis" significa coisas diferentes conforme o que muda, e ambas já
estão resolvidas — importa não as confundir.

**Alterar a apresentação.** Nova `versao_ndt`, aplicável aos documentos
produzidos a partir daí. Nenhum documento existente é tocado, e os já emitidos
continuam a renderizar-se com o template que declaram. É trivial por construção,
e é a razão de o NDT existir separado. Quanto mais apresentação estiver no NDT,
mais ágil é o sistema — ver §3.1 para o que isto garante e o que não promete.

**Alterar o documento.** Não existe. Um ato administrativo finalizado não se
edita: produz-se um novo, com uma relação de sucessão para o anterior
(`relacoes[{tipo: "substitui"}]`, ADR-011). É o que o direito já faz — um
diploma retificado não apaga o original; ambos existem e há uma relação entre
eles. A agilidade aqui não está em poder editar, está em o mecanismo de sucessão
ser barato, verificável e não exigir infraestrutura viva para ser interpretado.

Dito de outro modo: **a imutabilidade não é obstáculo à agilidade — é o que
torna a agilidade confiável.** Só se pode mudar depressa aquilo que se pode
mudar sem destruir prova.

## 6. Requisitos aplicáveis, por camada

Mapa indicativo, para verificar que nenhuma exigência fica sem camada
responsável. **Não é parecer jurídico**: a avaliação de conformidade legal está
sujeita ao gate de revisão externa previsto em
[`READINESS.md`](../normalization/READINESS.md).

| Exigência | Camada responsável | Estado |
|---|---|---|
| Assinatura eletrónica e sua validade a longo prazo (eIDAS) | envelope — CAdES-B-LTA, timestamps, material de validação | coberto |
| Proteção de dados pessoais | NDF `metadados.protecao_dados` | coberto |
| Avaliação e destino arquivístico | NDF `avaliacao` + perfis | coberto |
| Autenticidade e cadeia de custódia | envelope + Perfil de Ciclo de Vida | coberto (perfil opcional) |
| Acessibilidade digital | **NDT** (`alt`, `rotulo_acessivel`, ordem de leitura, PDF/UA-2) e **NCRTF** (`alt` em imagens) | parcial — depende do renderizador |
| Interoperabilidade e formatos abertos | projeções ODF e HTML a partir do mesmo NDT | parcial — renderizadores por implementar |
| Publicidade e legibilidade do ato | **NCRTF** (notas, remissões, articulado) e **NDT** (paginação) | **lacunas identificadas** — ver `ODF-ALIGNMENT-STUDY.md` |

A leitura útil: as exigências centradas na prova estão resolvidas no NDF; as
lacunas concentram-se nas camadas de apresentação e de estrutura de texto — que
é precisamente onde o trabalho atual está focado.

## 7. Teste de projeção

PDF, ODF, HTML e qualquer formato futuro são **expressões** do par NDF+NDT,
nunca a fonte. Três consequências operacionais:

1. **Nenhuma projeção pode ser fonte de verdade.** Um PDF assinado é prova de
   uma representação, não do documento.
2. **Quando duas projeções exigem coisas incompatíveis, ganha o modelo
   abstrato.** O NDT exprime a intenção; cada perfil de renderizador resolve-a
   como a sua tecnologia permitir.
3. **Uma funcionalidade que só faça sentido numa projeção não pertence ao NDT.**
   Já aplicado: o `modo` do campo de assinatura, específico do PDF, é
   explicitamente ignorado pelos renderizadores de fluxo (SPEC NDT §5.3.6).

Daqui decorre o **teste de longevidade**: se amanhã surgir um formato novo, o
par NDF+NDT deve projetar-se para ele sem alteração. Um conceito importado de
uma tecnologia concreta falha este teste. Um conceito derivado da natureza do
documento passa-o.

Isto não impede — antes recomenda — usar o ODF como inspiração. O ODF resolveu
estes problemas há duas décadas e é norma internacional aberta. Importa-se o
**modelo conceptual**; não se importa a **serialização**, nem os mecanismos que
existem para servir uma aplicação de escritório.

## 8. Teste de admissão

Antes de qualquer elemento novo entrar em qualquer camada:

1. **Caso de uso documentado.** Um documento real que hoje não se consegue
   exprimir. Sem isso, não entra — regra do ADR-015, já aplicada ao NDF.
2. **Camada determinada** pela hierarquia da cláusula 4, não pela conveniência
   de implementação.
3. **Verificabilidade.** Se é requisito, tem de ter identificador, evidência e
   caso de conformidade. Um requisito sem imposição é uma intenção — foi
   exatamente o que a ronda de conformação do NDT teve de corrigir.
4. **Aditividade.** Preferir MINOR aditivo. Uma alteração MAJOR exige
   justificação própria e plano de migração.

## 9. Casos resolvidos pelo critério

Aplicação a decisões concretas já discutidas, como validação do critério:

| Questão | Camada | Porquê |
|---|---|---|
| Família tipográfica de um parágrafo | **NDT** | Declara-se uma vez por template, em vez de ser copiada para dentro de cada documento (cláusula 3.1). Hoje está no NCRTF — a corrigir |
| "Este bloco é uma citação legal" | **NCRTF** | É o que a coisa é; faz parte do ato e não deve mudar |
| Nível 3 numera-se `a)` ou `i)` | **NDT** | É como se vê. O NCRTF declara que é nível 3 |
| Texto de uma nota de rodapé | **NCRTF** | É conteúdo do ato |
| Onde a nota aparece na página, e o seu separador | **NDT** | É apresentação |
| Alvo de uma remissão interna | **NCRTF** | O ato remete para si próprio; a remissão é parte do texto |
| Viúvas, órfãs, manter-junto | **NDT** | Qualidade de composição, não conteúdo |
| Marcas de revisão, comentários | **fora** | Estado de edição; não sobrevive à finalização |
| Data e autor mostrados no documento | **NDF** | São factos assinados. Duplicá-los no conteúdo criaria dados não assinados |
| Índice de conteúdos | **projeção** | Derivável dos títulos; gera-se, não se armazena |
| Estado do procedimento | **fora** | Sistema de gestão documental |
