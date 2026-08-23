# Captura documental e ingestão — desenho do ndfpkg

**Estado:** documento de desenho, não normativo. Nenhuma cláusula aqui é
requisito enquanto não for vertida para `specs/ndf/SPEC.md` com identificador
próprio e caso de conformidade.

**Origem:** brainstorming do responsável do projeto (2026-08-20) sobre a
extensão do `.ndfpkg` para documentos que não nascem no editor estruturado, e
revisão crítica subsequente. Substitui o handoff informal
`normordis-core-ingest-decisoes`, cuja parte de arquitetura de aplicação foi
separada para o repositório `normordis-kernel`.

---

## 1. O problema

O editor Lexical cobrirá a maioria dos documentos administrativos correntes,
mas não toda a riqueza de formatação ocasionalmente necessária. O fluxo atual
(`dotm` → `dotx`) responde a isso hoje. É preciso uma via para os casos que o
editor estruturado não cobre, sem transformar o NDF num formato universal que
interpreta semanticamente ODF, DOCX, PDF, imagens ou XML.

Existe além disso um segundo problema, independente do primeiro e mais amplo:
documentos que **chegam de fora** — requerimento digitalizado, submissão via
e-balcão, certidão de outra entidade, ficheiro anexo a correio eletrónico — e
cuja guarda é juridicamente necessária.

Os dois problemas foram tratados em conjunto no brainstorming. **São
distintos e admitem respostas de custo muito diferente**, e é essa separação
que estrutura o resto deste documento.

## 2. Decisão: PDF/A na via de produção interna

Quando um serviço precisa de formatação superior à do editor estruturado, o
documento é produzido no processador de texto que o serviço já usa
(LibreOffice, Word ou outro) e **exportado pelo próprio produtor como PDF/A**.
O NORMORDIS captura o PDF/A. Não captura o `.odt` nem o `.docx`.

### 2.1 O que a decisão resolve

| Problema que desaparece | Porquê |
|---|---|
| Canonicalizador server-side | Não é preciso LibreOffice headless no servidor, nem manter, atualizar e auditar essa dependência |
| Risco de fidelidade da conversão | A conversão é feita na ferramenta que é dona do formato, pelo autor, que **vê e aprova o resultado** antes de finalizar |
| Round-trip ODF ↔ estrutura | Não existe: nunca há transição entre os dois modos dentro do mesmo documento |
| Mapeamento ODF → NDT | Não se tenta. O NDT não é inventado a partir de um binário arbitrário |
| Dependência da estabilidade de renderização a 15 anos | PDF/A existe precisamente para isto; um `.odt` reaberto no LibreOffice de 2041 não oferece a mesma garantia |
| Dependência do processador de texto | A via é agnóstica: `.docx` e `.odt` seguem exatamente o mesmo caminho, sem adapter para nenhum |
| Distinção `source_original` / `canonical_representation` | Colapsa: nesta via, o PDF/A é simultaneamente o original e a representação congelada. **Um único componente** |

A decisão coloca ainda o congelamento da reconstituição no sítio certo. O
*freeze-at-signing* deixa de ser um passo automático do servidor sobre um
ficheiro que ninguém reviu, e passa a ser um ato do produtor, que confirma
visualmente o que está a emitir.

### 2.2 O que a decisão não resolve — e não deve tentar resolver

A decisão aplica-se à **produção interna**, onde o serviço controla a
ferramenta e pode exigir o formato de saída. Não se aplica à **receção
externa**, onde os bytes que chegaram *são* o documento e não é possível pedir
ao remetente que reexporte.

| Via | Entrada | Regra |
|---|---|---|
| Produção interna | documento redigido no serviço | **Só PDF/A.** Um componente. Sem captura do ficheiro de escritório |
| Receção externa | requerimento digitalizado, e-balcão, ficheiro de terceiro, correio eletrónico | **Preservar byte a byte o que chegou**, seja qual for o formato. Representação canónica só quando a fidelidade visual for relevante e o formato de origem não a garantir |

O modelo de componentes continua necessário para a segunda via. O que a
decisão de §2 faz é retirar-lhe a via de produção interna, que era o caso mais
frequente e o de maior custo de implementação.

### 2.3 O rascunho editável não é matéria de preservação

Perde-se a fonte editável: corrigir um documento finalizado implica refazê-lo,
não editá-lo. Isto é coerente com o princípio de imutabilidade (SPEC §2.1) e
com o mecanismo de sucessão (`relacoes[substitui]`, ADR-011) — um ato
finalizado nunca se edita, produz-se outro.

O ficheiro de trabalho vive no sistema de negócio **antes** da finalização,
fora do NDF, sob a política de retenção desse sistema. Não é objeto de guarda
documental. O serviço deve conhecer este custo prático antes de escolher a via.

### 2.4 Validação de formato na ingestão — dois regimes

**Decidido (2026-08-20).** A qualidade da exportação PDF/A varia entre
processadores e versões, e um ficheiro que se declara PDF/A pode não o ser. A
conformidade não deve ser inferida do nome nem da extensão.

O que o **formato** pode fazer é definir o lugar onde o resultado se regista.
Não pode obrigar ninguém a correr um validador, nem julgar o que recebe: o NDF
guarda o documento **tal como o sistema produtor o emitiu** (§7.4). As regras
seguintes são, portanto, política de ingestão recomendada, não requisitos de
conformidade NDF.

| Via | Não conformidade | Fundamento |
|---|---|---|
| Produção interna | **controlo de qualidade a montante da emissão** | O serviço é o produtor e pode reexportar **antes** de finalizar. Depois de emitido, guarda-se como foi emitido — a recusa é um travão do produtor sobre si próprio, não do formato sobre o produtor |
| Receção externa | **aceita-se sempre, com deficiência registada** | Ao contribuinte não se impõem formalidades além da autenticação no portal. Um JPG, um PDF simples ou um ficheiro malformado são o que chegou |

Na via externa, a deficiência é **propriedade do artefacto recebido, nunca
fundamento de recusa da submissão**. O ato de submeter produz efeitos jurídicos
independentemente da qualidade técnica do ficheiro; o registo da deficiência
serve a preservação, não o controlo de admissibilidade.

O registo tem de ser estruturado, não texto livre: formato declarado, formato
verificado, resultado, validador e sua versão, instante. Daqui a quinze anos,
«PDF não conforme» sem saber que validador e que versão o afirmaram é
informação inútil.

Isto é a aplicação do mesmo padrão de §7.3: o estado da estratégia de
reconstituição — adequada, adequada com deficiência, ou ausente — é sempre
representável e nunca silenciado.

### 2.4.1 Perfil PDF/A alvo — decidido (2026-08-20, Q3)

| Via | Regra |
|---|---|
| **Produção interna** | Mínimo exigível **PDF/A-2b**. RECOMENDADO PDF/A-2u (texto extraível) onde o produtor o suporte, por servir a pesquisa sem custo adicional |
| **Receção externa** | Qualquer parte e nível, ou nenhum. Regista-se o que é, não se exige nada |

Notas de escolha:

- **PDF/A-2b** é a linha de base arquivística com suporte real em LibreOffice e
  Word hoje. PDF/A-1b é aceite; não é o alvo por ser mais restritivo sem ganho
  de preservação.
- **PDF/A-3** é aceite, mas a sua capacidade de embeber ficheiros **não é usada**
  pelo NORMORDIS na via de captura: produziria um contentor dentro do contentor,
  com dois inventários e nenhuma regra de precedência.
- **PDF/A-4** (ISO 19005-4, sobre PDF 2.0) é o que alinha com o alvo PDF/UA-2 do
  NDT §8.2, mas o suporte nos produtores é hoje escasso. Admissível, não exigido.
  Reavaliar quando o suporte generalizar.

O registo é sempre **estruturado** — parte e nível de conformidade separados,
mais validador e versão — nunca a string `"PDF/A"`, que não identifica nada.

**Normalização arquivística** (converter um JPG recebido para TIFF ou PDF/A de
preservação) é decisão de política de arquivo, não do formato. Fica para o gate
externo 3, com a DGLAB.

### 2.5 Tensão com a tese central, a assumir explicitamente

O `README.md` declara: *«a fonte de verdade reside nos dados; o PDF é uma
projeção desses dados»*. Nesta via, **o PDF é a fonte de verdade**. Não há
dados estruturados a montante de que ele seja projeção.

É uma exceção legítima, mas tem de ser nomeada. Ver §3.

## 3. Um só formato, duas realidades

**Decidido (2026-08-20).** Não há dois formatos — um NDF para documentos
nativos e outro para importados. Há um NDF que cobre as duas realidades, com
limitações reconhecidas e declaradas no segundo caso.

Isto não é alargamento do formato: é o mecanismo que o NDF já tinha, exercido
pela primeira vez. SPEC §2.9.1 declara que o NDF-core é um **envelope
genérico** e que `documento` é **intencionalmente opaco** a esse nível, tipado
por schema próprio, para acomodar «qualquer tipologia futura […] sem
necessidade de revisão major desta especificação». `documento-capturado@1.0.0`
é uso desse mecanismo, não excepção a ele.

### 3.1 Precisão de vocabulário — `payload` não é o conteúdo

`payload_bytes` são os bytes JCS do **NDF-core completo** (SPEC §5.2, passo 1),
não do bloco `documento`. Dizer que «o documento capturado não tem payload» lê-se
como «não tem `payload_hash` nem base de assinatura», o que é falso.

Nos dois casos existe `payload_bytes`, existe `payload_hash`, existe
`validation_code`, e o CAdES assina exatamente a mesma coisa. **O que difere é
`documento`, e só ele.**

### 3.2 O que é rigorosamente igual

`ndf_id` · `estado` · `nivel_assinatura` · `payload_hash_alg` · `metadados` ·
`avaliacao` · `relacoes` · `participantes` · `imputacao` ·
`proveniencia_sistema` · `proveniencia_ia` · envelope CAdES-B-LTA com
timestamps e material de validação · `validation_code` · cadeia de custódia.

Ou seja: quase todo o NDF. **Um NDF capturado não é um NDF degradado** — é um
NDF completo cujo `documento` aponta para fora em vez de conter o texto do ato.
A diferença está confinada a um bloco.

### 3.3 O que difere — duas coisas, não uma

**`documento`.** No nativo contém o ato. No capturado contém a casca descritiva
(§3.9) mais `componentes[]`: a identificação do ato sobrevive, o corpo do ato
desce para dentro do binário.

**`ndt_version_ref` muda de função.** No nativo o NDT é **gerativo** — a
instrução a partir da qual o documento se produz visualmente. No capturado é
**descritivo** — renderiza o auto de captura (§5), não o documento. É esta
diferença que quebra, nesta via, o princípio do `README.md` de que o PDF é uma
projeção dos dados.

### 3.4 Leitura por camadas

Em termos da hierarquia de [`CRITERIO-DE-CAMADAS.md`](CRITERIO-DE-CAMADAS.md) §4:

| Camada | Nativo | Capturado |
|---|---|---|
| 1 — factos sobre o documento | NDF `metadados` e blocos próprios | **igual** |
| 2 — conteúdo que comunica | NDF `documento` | reduzido à identificação do ato |
| 3 — estrutura semântica | NCRTF | dentro do binário |
| 4 — apresentação | NDT | dentro do binário |
| 5 — prova | envelope + custódia | **igual** |

**A captura colapsa as camadas 2, 3 e 4 num único artefacto opaco, e mantém
intactas a 1 e a 5.**

E o que torna as duas vias equivalentes em prova: o conteúdo não está dentro
dos bytes assinados, mas está **amarrado a eles pelo hash** — desde que
`componentes[].sha256` viva em `documento` e não no manifesto (§4).

### 3.5 O que se perde, com precisão

Não é a reconstituição — um PDF/A reconstitui-se bem. É a **projetabilidade**:

- reprojeção para outro meio (ODF, HTML, corpo grande para acessibilidade,
  extração estruturada). `CRITERIO-DE-CAMADAS.md` §7 chama-lhe teste de
  longevidade; o documento capturado **falha-o por construção**;
- consulta ao nível do campo sobre o conteúdo do ato;
- alteração central de apresentação para documentos futuros do mesmo tipo.

A via capturada é igual em custódia e integridade, e estritamente mais fraca em
capacidade. Não ganha nada em troca exceto tolerar entrada arbitrária — que é
exatamente aquilo para que existe.

A afirmação de que as duas vias «não distinguem cidadãos ou serviços conforme a
via de produção» **não é sustentável** e não deve ser comunicada. A distinção é
verificável por inspeção: `metadados.tipo_documento_ref` igual a
`documento-capturado@<versao>`.

### 3.6 O que a unidade de formato compra

Não é elegância. É, concretamente:

| Ganho | Porquê importa |
|---|---|
| **Um só grafo documental** | Um despacho nativo faz `decide_sobre` um requerimento capturado pelo mesmo mecanismo, com o mesmo vínculo por `payload_hash`. Dois formatos exigiriam uma ponte — e as pontes apodrecem |
| **Um só regime arquivístico** | `avaliacao` (PCA/DF, perfil, instrumento) aplica-se identicamente. O arquivo vê uma classe de objetos, não duas. Decisivo para o gate externo 3 |
| **Uma só cadeia de custódia** | `custody-event.schema.json`, indexado por `ndf_id`, serve os dois sem alteração |
| **Um só verificador** | Um terceiro valida qualquer `.ndfpkg` com o mesmo código. Dois formatos seriam duas suites de conformidade — e a segunda ficaria sempre atrás |
| **Uma só afirmação jurídica** | `imputacao`, `nivel_assinatura` e `validation_code` significam o mesmo independentemente da origem |
| **Corpus homogéneo através da transição** | Quando o editor passar a cobrir um tipo (§8), os documentos nativos são o **mesmo tipo de objeto** que os capturados que os precederam. Dois formatos deixariam uma costura permanente no arquivo |

O último é o mais forte, e liga-se diretamente ao regime de transição de §8: a
unidade de formato é o que permite que a transição seja gradual em vez de
produzir dois arquivos paralelos.

### 3.7 A estrutura arquivística não é o prémio de consolação

Vale inverter a leitura habitual. O que o NDF entrega — identidade, proveniência,
imputação, avaliação, fixidez, relações, custódia — **é o mesmo nos dois casos, e
é a proposta de valor principal em ambos**. O nativo acrescenta a isso a projeção
determinística a partir de dados.

Dito de outro modo: a estrutura arquivística não é o que sobra quando não se
pode ter mais; é a coisa primária, e a projetabilidade é o extra do caminho
nativo. Isto é também o que a arquivística já faz há décadas — descreve com o
mesmo aparelho descritivo registos born-digital estruturados e imagens
digitalizadas.

### 3.8 O preço da unidade, a pagar deliberadamente

Dois formatos tornariam a diferença óbvia pelo nome. Um só formato torna
possível **alegar para um documento capturado garantias que só o nativo tem**,
porque o rótulo é o mesmo. É o único argumento sério a favor da separação, e
descartá-lo em silêncio seria leviano.

A unidade continua a ser a escolha certa, mas desloca o ónus para a conformidade
e para a comunicação. Consequência concreta a fixar em SPEC §9.2: **um leitor
conforme NÃO DEVE tentar renderizar um documento capturado aplicando o seu NDT a
`documento` como se fosse conteúdo** — tem de resolver o componente. Sem um
requisito `NDF-READ-*` deste teor, «um formato» degenera em «um formato com dois
comportamentos silenciosos».

Cautela adjacente: manter **um** tipo genérico `documento-capturado@1.0.0`, não
uma família (`oficio-capturado`, `parecer-capturado`, …). O campo
`tipo_equivalente` (§3.9) transporta a correspondência sem duplicar o registo.

### 3.9 De onde vêm os metadados de um documento capturado

Num NDF nativo, os dados descritivos e o conteúdo têm origem única: o mesmo ato
de edição produz ambos. Num capturado, não. O conteúdo é opaco e os metadados
têm de ser **afirmados separadamente** — por preenchimento humano na ingestão,
ou por proveniência de submissão quando o canal a fornece (e-balcão: submissor
autenticado, instante de entrada, número de protocolo).

Consequência estrutural: `documento-capturado@1.0.0` é, na prática, **a mesma
casca descritiva de um tipo nativo com o corpo substituído por uma referência
binária**. Comparado com `oficio@1.0.0` (SPEC §2.9.3), tem `numero`, `data`,
`assunto`, `destinatario` — e, em vez de `corpo`, `componentes[]`. Isto mantém
o capturado indexável e pesquisável pelos mesmos campos que o nativo, que é
precisamente o que o serviço precisa.

**Risco a assumir: divergência silenciosa.** Os metadados afirmam «Ofício
123/2026 de 15-06» e o PDF pode dizer outra coisa. Nada o impede, porque são
duas asserções independentes. Num nativo isso não pode acontecer.

Regra de resolução, a tornar normativa: **em conflito, o binário é
autoritativo quanto ao conteúdo do ato; o NDF é autoritativo quanto à
identidade, custódia e classificação.** Nenhum dos dois corrige o outro — um
erro de metadados corrige-se por novo NDF com `relacoes[corrige]`, nunca por
edição.

**Colocação normativa — decidida (2026-08-20, Q6):** a regra entra na cláusula
§2.8 alargada (tarefa C1), junto da admissão de componentes por hash. É uma
regra de **leitura** de um documento cujo conteúdo é um componente, pelo que
pertence ao mesmo sítio onde essa possibilidade é aberta — não a §2.9
(tipologias), que trata da estrutura de `documento`, nem ao registo, que não é
lugar de regras de interpretação.

Mitigação parcial e barata: extrair texto do PDF na ingestão e verificar se os
valores-chave (número, data) nele ocorrem. Não é conclusivo, mas apanha erros
grosseiros. Deve produzir **aviso**, nunca recusa — e o texto extraído é dado
derivado, fora do NDF (§7.1).

**Campo opcional `tipo_equivalente`.** Registar qual o tipo nativo que o
documento teria se tivesse sido produzido no editor estruturado. É a métrica
que permite saber, por tipo, que proporção do corpus ainda passa pela via
capturada — e, portanto, onde investir a seguir no editor (§8). Opcional
justamente porque nem sempre é determinável.

## 4. Onde vivem os componentes — e porque não no manifesto

**Esta é a correção mais importante ao desenho recebido.**

O brainstorming propôs sucessivamente duas colocações para a declaração dos
binários: primeiro `payload_ref` no **envelope**, depois `components[]` no
**manifest.json**. As duas falham pela mesma razão.

A assinatura CAdES é *detached* sobre `payload_bytes`, que são os bytes
canónicos do **NDF-core** e apenas esses (SPEC §5.2, passos 1 e 4). O envelope
*contém* a assinatura, não é coberto por ela. O `manifest.json` também não —
e a própria SPEC §8.3 diz que o manifesto é inventário físico e **não deve**
duplicar informação documental do NDF-core.

Consequência prática: se o `sha256` do PDF/A só existir no manifesto, trocar o
PDF e regerar o manifesto produz um pacote que passa em toda a validação
existente. Num documento capturado, **o binário é o documento** — a promessa de
preservação ficaria sem fundamento criptográfico.

Isto desfaz, sem que ninguém tenha notado, o melhor resultado do próprio
brainstorming: a afirmação de que a representação congelada fica «coberta pela
mesma assinatura CAdES-B-LTA» só é verdadeira se o seu hash estiver dentro de
`payload_bytes`.

**Colocação correta:** os componentes são declarados em `documento`, através do
schema do tipo `documento-capturado@1.0.0`:

```json
{
  "documento": {
    "componentes": [
      {
        "id": "principal",
        "papel": "representacao_congelada",
        "media_type": "application/pdf",
        "perfil": "PDF/A-2b",
        "sha256": "sha256:...",
        "tamanho": 352991,
        "nome_original": "parecer.pdf"
      }
    ]
  }
}
```

Isto:

- fica dentro de `payload_bytes`, logo canonicalizado e assinado;
- **não altera o NDF-core** — é `tipo_documento_ref` mais schema próprio, que
  o `ROADMAP.md` classifica expressamente como não sendo alteração de formato;
- passa o teste de admissão de novas primitivas no passo 2, sem reabrir D5;
- dispensa alterar `manifest.schema.json`.

**O manifesto provavelmente não precisa de mudar.** `tools/validate.py` já
exige que todo o ficheiro presente no pacote esteja inventariado com hash
correto, e `PKG-NEG-002` rejeita ficheiros não inventariados. A integridade
física de um binário em `original/` já está coberta pelo mecanismo existente.
O que falta é a declaração *documental* — papel, tipo, identidade — e essa
pertence a `documento`.

**Nunca** incluir referência de storage, bucket, URI ou nome de adapter. Essa
crítica do brainstorming está inteiramente correta: amarraria o documento à
infraestrutura que o custodia hoje e contradiria a razão de ser de uma
especificação CC0.

A junta verificável nova, e o único requisito `NDF-PKG-*` realmente necessário,
é a coerência entre `documento.componentes[].sha256` e `manifest.inventario`.

## 5. `ndt_version_ref` e o auto de captura

`ndt_version_ref` é obrigatório no NDF-core (`ndf-core.schema.json`,
`required`) e `tools/validate.py` falha se o NDT referenciado não estiver no
pacote. Um documento capturado não tem template declarativo.

**Solução:** um NDT canónico `documento-capturado@1.0.0` que renderiza um
**auto de captura** — frontispício com `ndf_id`, `validation_code`,
proveniência de submissão, inventário de componentes com hashes e resultado da
validação de formato. Resolve o campo obrigatório sem tocar no core e produz um
artefacto genuinamente útil.

Tornar `ndt_version_ref` opcional seria alteração major do core e deve ser
rejeitado.

## 6. Assinaturas: CAdES, PAdES e o que não se herda

[`specs/ndt/SPEC.md`](../../specs/ndt/SPEC.md) §8.1 já fixa a doutrina: o CAdES
do envelope assina os `payload_bytes`; uma assinatura PAdES assina os bytes do
PDF pelo seu `ByteRange`; podem usar o mesmo certificado mas são operações,
valores e timestamps distintos. Aplicada à captura:

**PAdES que chega de fora** — preservado byte a byte, **nunca reescrito**. É a
regra já assente para PDF assinado externamente.

**PAdES produzido internamente** — opcional, e é conveniência de distribuição
(um PDF que circula fora do NORMORDIS mostra validade num leitor comum), não a
prova canónica. Se for produzido, **a ordem importa**: assinar o PDF, calcular
o hash do PDF já assinado, ancorar esse hash no NDF-core, finalizar o NDF. A
ordem inversa produz um hash que não corresponde ao ficheiro distribuído.

**`nivel_assinatura` nunca se herda de um componente.** Descreve a assinatura do
NDF. Um capturado que contenha um PDF com assinatura qualificada de terceiro
pode perfeitamente ter `nivel_assinatura: "nenhuma"` com selo institucional. A
regra deve ser normativa e explícita, sob pena de leitura errada.

### 6.1 A validade de uma assinatura externa decai

Preservar os bytes não preserva a verificabilidade. Uma assinatura qualificada
de terceiro torna-se inverificável quando os certificados expiram, se ninguém
tiver congelado a cadeia, os dados de revogação e o timestamp **no momento da
captura** — é exatamente o problema que o nível LTA resolve para as assinaturas
próprias e que aqui não tem equivalente automático.

É este o conteúdo do diretório `evidence/`, que o desenho recebido nunca
definiu: material de validação da assinatura externa, recolhido na ingestão,
hasheado e declarado como componente. Sem isto, «preservação da assinatura
externa» é uma promessa que caduca.

## 7. Fronteiras a manter

### 7.1 Texto extraído é dado derivado, não conteúdo

O brainstorming sugeriu usar NCRTF como extração de texto do binário para
indexação e pesquisa. **Não deve entrar no NDF-core.**

Uma extração é lossy e recalculável. Em `documento`, entraria em
`payload_bytes` e ficaria assinada como se fosse o conteúdo do ato — que não é.
Se a extração melhorar (melhor parser, melhor OCR), o documento assinado fica
com a versão pior para sempre, ou obriga a novo NDF por um motivo que não é
documental.

O precedente e o nome já existem: SPEC §3.6, «dados derivados (fora do
NDF-core)» — operacionais, recalculáveis, não assinados. Índice de pesquisa é
isso. Fora do NDF e fora do pacote legal.

### 7.2 Sugestão de classificação é estado de workflow

A regra decidida — a IA sugere, só a validação humana torna a classificação
autoritativa — está certa e não é exceção nova: é a política já estabelecida em
SPEC §2.13.4 aplicada à classificação.

Mas o bloco `suggestion` **não deve entrar no NDF-core**: é estado de
procedimento e falha o passo 1 do teste de admissão. Vive no workflow/auditoria
do sistema de gestão.

O formato já tem o recetáculo para o que resta depois da validação:
`proveniencia_ia` com `finalidade: "classificacao"` e `revisao_humana.estado`
(SPEC §2.13.3), incluindo o valor `"pendente"`, que torna a ausência de revisão
representável em vez de omitida. Nada de novo é preciso.

### 7.3 Estratégia de reconstituição ausente tem de ser representável

A regra generalizada — gera-se representação canónica quando a fidelidade
visual for relevante e o formato de origem não a garantir — não prevê o caso em
que **devia gerar-se e não foi possível**: formato obsoleto, ficheiro cifrado,
original corrompido.

Omitir silenciosamente transforma um risco conhecido em risco invisível. O
repositório já resolveu isto duas vezes com o mesmo padrão:
`revisao_humana.estado: "pendente"` (§2.13.3) e `destino_final:
"a_determinar"` (§3.4.1).

Precisão de fronteira (§7.4): **ter** estratégia adequada é dever do produtor e
de quem opera a ingestão; o formato não o impõe nem o verifica. O que o formato
deve é tornar o estado **expressável** — adequada, adequada com deficiência, ou
ausente — para que a omissão não passe por silêncio.

### 7.4 O dever do formato, e o que não lhe compete

**Dever do formato (responsável, 2026-08-20):** o formato deve permitir que
**toda a informação relevante e necessária possa ser guardada e reproduzida**.
É esse o seu dever, e é só esse.

Daqui saem duas obrigações simétricas, que convém não trocar:

| | Dever de quem |
|---|---|
| **Capacidade de representação** — existir lugar para tudo o que é relevante e necessário | **do formato** |
| **Correção do que se representa** — que o declarado seja verdadeiro, competente, completo e legal | **do produtor** |

Se algo relevante não tem onde ser guardado, é lacuna do formato e resolve-se no
formato. Se tem lugar e vem mal preenchido, não é problema do formato.

Este critério é o **complemento em falta** do teste de admissão de novas
primitivas do [`ROADMAP.md`](../../ROADMAP.md) (2026-08-15): aquele decide o que
**não entra** no core; este decide o que **tem de ser possível**. Juntos, limitam
o formato pelos dois lados — sem o segundo, o primeiro só sabe dizer que não.

Aplicado ao trabalho desta sessão, confirma três achados: os
`componentes[].sha256` têm de poder viver nos bytes assinados (§4); a ausência
de estratégia de reconstituição tem de ser expressável (§7.3); e a cadeia de
custódia hoje **não pode** acompanhar uma transferência (§11.2, L-T2) — sendo
relevante e necessária, isso é lacuna do formato, não da operação.

**Corolário (reafirmado pelo responsável, 2026-08-20).** O NDF não substitui a
responsabilidade dos sistemas produtores, e **guarda o documento tal como o
sistema produtor o emitiu**. No limite, um produtor pode emitir um documento
juridicamente incompleto e o NDF ser válido. A responsabilidade é do produtor,
não do formato.

Não é doutrina nova. SPEC §1.1 declara que a validade jurídica «não é garantida
pelo formato isoladamente»; §1.4 e §2.13.1 dizem o mesmo quanto a RGPD e AI
Act; `LACUNAS.md` L1 regista que `relacoes[]` prova integridade, não
legitimidade; o `README.md` remete alegações jurídicas para avaliação
competente. O que é novo é aplicá-la à captura, onde a tentação de «melhorar» o
que se recebe é maior.

**Fidelidade ao emitido.** O sistema não corrige, não normaliza, não completa e
não reescreve. Já era regra para PDF assinado (§6) e para `payload_bytes`
(SPEC §5.3); passa a ser regra geral da captura. Uma deficiência detetada
regista-se (§2.4); não se emenda.

**O teste operacional:** *um verificador consegue decidir isto tendo apenas o
pacote em mãos?*

| Pode ser requisito do formato | Não pode |
|---|---|
| **Estrutural** — o campo existe e tem esta forma | Que o valor declarado seja **verdadeiro** |
| **Consistência interna** — o hash bate com os bytes, `ndt_version_ref` resolve, `componentes[].sha256` bate com o inventário | Que o signatário tivesse **competência** para o ato |
| **Semântico-declarativo** — este campo significa isto, não inferir além disso | Que a classificação atribuída seja a **correta** |
| **Comportamento de leitor** — não renderizar um capturado aplicando o NDT a `documento` (§3.8) | Que estejam presentes **todos os anexos** que a lei exige |

Se a decisão exige o mundo — a lei, a orgânica, o procedimento, os factos — é do
produtor. Se se decide dentro do artefacto, pode ser conformidade.

**Consequência a comunicar, não a esconder:** um `.ndfpkg` válido não é garantia
de legalidade, completude nem correção — é garantia de integridade, identidade e
interpretabilidade.

### 7.4.1 Existência do ato e validade do ato

O paralelo com o papel é exato. Um documento em papel pode ser assinado por
quem não tem competência: o ato **existe**, produz efeitos, e a sua validade é
decidida pelas autoridades próprias, administrativas e judiciais. O suporte
nunca decidiu isso — nem o papel, nem o NDF.

O que muda a favor do NDF é o que fica disponível para essa decisão posterior.
Quando a autoridade anula, a anulação é ela própria um documento, ligado ao
original por `relacoes[{tipo: "anula"}]` (SPEC §2.11.2), e **o original é
preservado intacto** em vez de substituído. Na prática de papel, o documento
viciado é frequentemente retirado e substituído, e o rasto perde-se. O formato
não julga o ato; preserva o que permite julgá-lo, e regista o julgamento como
facto documental de pleno direito.

### 7.4.2 O que o formato melhora — o mesmo teste, do lado positivo

O teste de §7.4 não serve só para limitar. As duas colunas são complementares:
aquilo que um verificador decide com o pacote em mãos é exatamente aquilo que o
formato pode **impor** e, portanto, melhorar.

| Contributo real para a qualidade | Onde vive |
|---|---|
| Completude estrutural do tipo — campos obrigatórios, `additionalProperties: false` | schema de `tipo_documento_ref` (SPEC §2.9) |
| Recusa de finalização com avaliação irresolúvel, nível de assinatura sem certificado conforme, ou tipos proibidos | pré-condições de finalização (SPEC §5.1) |
| Menção de imputação jurídica, frequentemente ausente ou implícita em prática de papel | `imputacao` (SPEC §2.15) |
| Proveniência de sistema e de IA declaradas | §2.13, §2.14 |

Isto é normalidade estrutural, não legalidade substantiva — mas é normalidade
que o percurso `Word → impressão → assinatura` não tem forma de garantir nem de
medir.

**Como formular a alegação sem a exagerar.** «Melhora a qualidade dos atos» é
empírico e cai sob os gates de `READINESS.md`; sem corpus comparativo (`R6`) é
alegação, não evidência. A versão defensável é mais estreita e mais forte:
**completude estrutural mensurável, onde antes não havia nada a medir** — a
proporção de documentos com `imputacao` presente, `avaliacao` resolvida ou
fundamentação não vazia é contável no NDF e incontável em papel.

### 7.4.3 Um risco sistémico, três manifestações

O mesmo perigo aparece em três sítios distintos: **passar validação estrutural
ser lido como correção substantiva**.

1. `validation_code` que confere — dá impressão de aval oficial;
2. um só formato para duas realidades — o rótulo igual sugere garantias iguais
   (§3.8);
3. formulário que valida a verde — ensina o operador que fez bem, quando só se
   verificou a forma. Em papel ninguém julga que o impresso o está a corrigir.

Três instâncias do mesmo problema pedem uma resposta única, não três remendos:
**uma doutrina de projeto sobre o que o NORMORDIS diz quando algo passa** —
nunca «válido» sem dizer o que foi verificado. Não é matéria de formato; é
matéria do projeto, e fica registada.

### 7.5 Vocabulário de relações

O enum de `relacoes[].tipo` é fechado (SPEC §2.11.2). `anexa` e `responde_a`
existem; **`instrui` não existe** e `resposta_a` está grafado errado no
material recebido. Via disponível sem revisão minor: extensão qualificada
`ext.<entidade>.instrui` (ADR-008, §2.11.7).

### 7.6 Eliminação de componentes

`CUST-REQ-003` fala em destruir `payload_bytes`. Se `destino_final:
"eliminacao"`, os componentes binários também têm de ser destruídos e o facto
registado no log de custódia. Lacuna a fechar em `custody-event.schema.json`.

## 8. Governação da via capturada — regime de transição

**Decidido (2026-08-20).** A pergunta não é «autorizar ou não a via
capturada». Hoje o editor estruturado ainda não cobre a maioria dos casos e o
fluxo real dos serviços é `Word → PDF`. Enquanto o editor evolui — o que levará
anos —, a via capturada **não é uma saída de emergência: é o regime maioritário
de um período longo de transição**.

Isto inverte o risco que eu tinha formulado. O perigo não é que as pessoas
fujam do caminho estruturado, porque ele ainda quase não existe. O perigo é
que, quando o editor passar a cobrir um tipo documental, **nada puxe esse tipo
de volta**. Uma autorização estática por tipo, decidida hoje, não resolve isso:
ou é permissiva demais agora e nunca aperta, ou é restritiva demais e bloqueia
trabalho real.

O instrumento adequado é diferente — **o registo de tipos documentais, que já é
versionado**, declara para cada tipo qual a via predefinida e se a captura é
admissível. À medida que o editor passa a cobrir um tipo, a entrada desse tipo
transita de «captura admissível» para «só estruturado», por nova versão do
registo. A transição faz-se tipo a tipo, com data e responsável, sem
big-bang e sem invalidar nada do que já foi produzido.

Três consequências práticas:

1. **A decisão é do registo, não do utilizador.** Nunca uma opção permanente no
   fluxo de criação, escolhida documento a documento — é isso que faria a via
   fácil vencer sempre.
2. **A proporção estruturado/capturado por tipo é a métrica de progresso**, e é
   trivial de obter: `metadados.tipo_documento_ref` já a permite contar, e
   `tipo_equivalente` (§3.9) afina-a. Diz, com dados, onde investir a seguir no
   editor — a transição deixa de ser intenção e passa a roadmap.
3. **A via capturada não é um estado inferior a esconder.** Tem de funcionar
   plenamente: metadados, segurança, auditoria, custódia, relações, avaliação
   arquivística. É precisamente o que o NDF acrescenta a um binário que, sem
   ele, seria só um ficheiro numa pasta. O que não pode é ser apresentada como
   equivalente em reconstituição (§3).

O que continua a merecer registo como risco: se a métrica do ponto 2 não for
efetivamente olhada, o regime de transição converte-se em regime permanente por
inércia — e o resultado é indistinguível de nunca ter havido governação.

## 9. Plano de ação revisto

A decisão de §2 reduz substancialmente o trabalho face ao plano inicial: cai o
canonicalizador, cai o adapter ODF, cai a dualidade original/representação na
via interna.

**Fase 0 — decisões prévias**
1. Decidir a governação de §8 (autorização por tipo documental). Bloqueia o
   valor de tudo o resto.
2. Decidir a política de PDF/A não conforme na ingestão (§2.4).
3. Registar no `ROADMAP.md` que o alargamento de SPEC §2.8 — que hoje exclui
   pela negativa os anexos binários opacos — é decisão de âmbito, à imagem da
   reabertura de D5 de 2026-08-13, e não clarificação editorial.

**Fase 1 — fundamentação normativa** (sem código nem schema)
4. ADR: componentes declarados em `documento`, com o argumento da assinatura (§4).
5. ADR ou secção: `nivel_assinatura` não se herda de componentes (§6).
6. Estudo de mapeamento PREMIS/METS ↔ `papel`, fechando parte de `R13`
   (depósito OAIS) e preparando o gate externo 3.

**Fase 2 — tipo documental e NDT de captura** (aditivo, core intacto)
7. `specs/registry/schemas/documento-capturado.schema.json`.
8. NDT canónico `documento-capturado@1.0.0` — auto de captura (§5).
9. Extensão qualificada `ext.<entidade>.instrui` documentada (§7.5).

**Fase 3 — pacote e conformidade**
10. SPEC §8.1: diretórios `original/`, `representacoes/`, `anexos/`,
    `evidencias/`; requisito de coerência `componentes[].sha256` ↔
    `manifest.inventario`.
11. Exemplo completo `specs/ndf/examples/captura-requerimento/`.
12. Vetores negativos: componente declarado ausente; hash divergente entre
    `documento` e inventário; ficheiro em `original/` não declarado; original
    reescrito.
13. Regenerar `REQUIREMENTS.md`, `TRACEABILITY.md`, `NORMATIVE-STATEMENTS.md`.

**Fase 4 — custódia**
14. Eventos de captura e de eliminação de componentes (§7.6).
15. Verificação periódica de fixidez no Perfil de Ciclo de Vida (SPEC §9.5),
    não no formato base.

**Sequenciamento — revisto (2026-08-20).** Fases 0 e 1 são documentais e podem
correr já.

A recomendação anterior de colocar as Fases 2 a 4 atrás de `normordis-pdf`
deixa de fazer sentido, por uma razão simples: **a via capturada não precisa de
renderizador**. O PDF já existe. Não compete com `R8` por trabalho, não depende
dele, e não usa nada do que ele produz.

Daqui decorre uma observação de oportunidade que não estava no plano inicial: a
via capturada é provavelmente **o caminho mais rápido até um utilizador real**.
Um serviço pode começar a capturar `Word → PDF` e obter já identidade,
metadados, auditoria, custódia, relações e avaliação arquivística, sem esperar
pelo renderizador. Ora, é exatamente utilizador real o que o
`READINESS-ASSESSMENT` identifica como faltando (`R5`, gate externo 7), e não
mais âmbito normativo.

Nota de fronteira: isto **não** substitui `R8`. A condição de abertura de
PR-001 é `normordis-pdf` a produzir documento a partir de NDF+NDT, e a captura
não a satisfaz — nem deve ser apresentada como se a satisfizesse.

## 10. Questões em aberto

| # | Questão | Quem decide |
|---|---|---|
| ~~Q1~~ | ~~Autorização da via não estruturada~~ | **decidido 2026-08-20** — regime de transição gerido pelo registo de tipos (§8) |
| ~~Q2~~ | ~~Formato não conforme na ingestão~~ | **decidido 2026-08-20** — dois regimes: recusável na produção interna, sempre aceite com deficiência registada na receção externa (§2.4) |
| ~~Q3~~ | ~~Perfil PDF/A alvo~~ | **decidido 2026-08-20** — PDF/A-2b mínimo interno; qualquer coisa aceite na receção externa (§2.4.1) |
| Q4 | Limite prático de dimensão da materialização (scan extenso, gravação) | operação |
| ~~Q5~~ | ~~Alargamento de SPEC §2.8~~ | **decidido 2026-08-20** — decisão de âmbito registada em `ROADMAP.md`; sem alteração ao NDF-core |
| ~~Q6~~ | ~~Onde a regra de divergência se torna normativa~~ | **decidido 2026-08-20** — na §2.8 alargada, tarefa C1 (§3.9) |
| ~~Q7~~ | ~~Quem olha a métrica estruturado/capturado~~ | **fechada 2026-08-20** — não aplicável até à primeira instalação real; contrato do indicador fixado no registo §3.2.6, roquete de §3.2.3 mitiga o risco de fundo |
| ~~Q8~~ | ~~Redação de `autor` em §2.12.2 face ao documento capturado~~ | **decidida 2026-08-20** — referente alargado ao componente; sem alteração de schema nem do invariante |
| ~~Q9~~ | ~~Quarto modo de origem~~ | **decidida e executada 2026-08-20** — `metadados.origem_nao_identificavel` com `fundamento` obrigatório; ADR-023, decisão de âmbito no `ROADMAP.md` |
| **Q10** | **`proveniencia_ia.utilizada: true` satisfaz o invariante de origem mesmo quando a IA apenas reviu ou classificou** | imprecisão anterior a este trabalho; registada, não corrigida |

## 11. Transferência entre entidades — âmbito adjacente

Registo de achados, não desenho. O objetivo declarado pelo responsável
(2026-08-20) é que um serviço possa remeter a outro um `.ndfpkg` contendo o
documento principal, os anexos e a cadeia de evidência e custódia relevante.

**Observação de enquadramento:** transferência entre entidades e depósito
arquivístico conforme OAIS são **o mesmo problema** — entregar uma unidade
autocontida, verificável e descrita a quem não partilha a nossa infraestrutura.
Resolver um resolve o outro, e é exatamente a pergunta que `R13` deixou em
aberto e que um arquivista competente fará (gate externo 3).

### 11.1 O que já viaja

Verificação offline da assinatura CAdES-B-LTA sem contactar o sistema
produtor; `validation_code` conferível por humano; schemas do tipo e do perfil
de avaliação dentro do pacote (§8.1), pelo que `documento` e `avaliacao`
validam sem acesso ao registo canónico; relações reconstituíveis a partir do
`ndf-core.json` de cada pacote (§6.3). É muito, e é o mais difícil.

### 11.2 O que não viaja — quatro lacunas

**L-T1 — Não existe conjunto de transferência.** Um `.ndfpkg` é **um**
documento. Anexos sem identidade própria viajam como componentes; anexos com
identidade própria são NDF autónomos, logo pacotes separados. Enviar «o
processo» é enviar N pacotes, e **nada declara quais compõem o conjunto nem
permite ao recetor saber se o recebeu completo**. É a lacuna maior, e é
precisamente o SIP de OAIS.

**L-T2 — A cadeia de custódia não faz parte do pacote.** A composição de §8.1
não inclui o log de custódia, que vive no Perfil de Ciclo de Vida (§9.5),
opcional. «Cadeia de custódia relevante» é hoje exatamente o que **não** é
transferido. E não basta acrescentar um diretório: exportar o log integral
divulga informação operacional interna (quem acedeu, quando). Há que separar o
que é **evidência transferível** — finalização, selagens, verificações,
transferências — do que é **auditoria interna**.

**L-T3 — Transferir custódia é um ato, não um envio.** `event_type:
"transferido"` já existe no schema de custódia, mas não há artefacto de
receção/aceitação pela entidade recetora. Sem ele, «enviado de forma segura» é
propriedade do transporte, não da custódia.

**L-T4 — Divulgação parcial é impossível por construção.** Um NDF é imutável e
assinado: não se pode remeter uma versão expurgada sem quebrar a assinatura. A
granularidade do que se envia é o documento inteiro ou nada. **Isto é o
comportamento correto**, coerente com a imutabilidade — mas obriga a que
divulgação parcial seja resolvida por **novo documento** (certidão, extrato)
com relação tipada ao original, nunca por mutilação do pacote. Deve ser
afirmado, não deixado a descobrir.

### 11.3 Duas dependências que o formato não deve prover

Verificar a assinatura prova integridade e identidade do signatário. Não prova
competência para praticar o ato, nem torna resolúveis os identificadores de
`entidade_produtora`, do registo de tipos ou do perfil de avaliação — é a
lacuna `L1` de [`LACUNAS.md`](../../LACUNAS.md), ampliada à escala
interinstitucional. Registos e listas de confiança são infraestrutura; o
formato faz bem em não os fornecer, mas a visão precisa de quem os forneça.

Dimensão é a segunda: com captura, um conjunto de transferência é um problema
de transferência de ficheiros, não de API (§10, Q4).

### 11.4 Consequência para prioridades

O conjunto de transferência (L-T1) e a evidência transferível (L-T2) valem
provavelmente mais, agora, do que mais detalhe de captura: são o que torna a
visão demonstrável, o que fecha `R13` e o que abre a conversa com a DGLAB
(`R5`). Merecem documento de desenho próprio.

> **Executado (2026-08-23):** [`NDF-CONJUNTO-DE-TRANSFERENCIA.md`](NDF-CONJUNTO-DE-TRANSFERENCIA.md)
> desenha L-T1 a L-T3 dentro da fronteira de
> [ADR-024](../architecture/ADR-024-fronteira-oais-modelo-de-informacao.md), e
> deixa três pontos de decisão (`D-XFER-1` a `D-XFER-3`) por fechar. L-T4
> confirma-se como comportamento correto, e a sua regra passa a governar o
> desenho da evidência de custódia.

## 12. Referências

- `specs/ndf/SPEC.md` §2.8, §2.9, §2.11, §2.13, §3.6, §4.1, §5.2, §8
- `specs/ndt/SPEC.md` §8.1 (CAdES vs PAdES), §8.2 (PDF/UA-2)
- `ROADMAP.md` — D5, teste de admissão de novas primitivas (2026-08-15)
- `LACUNAS.md` — princípio de âmbito
- [`CRITERIO-DE-CAMADAS.md`](CRITERIO-DE-CAMADAS.md) §3.1, §4, §7, §8
- `docs/reports/READINESS-ASSESSMENT.md` — `R8`, `R13`
- `docs/interoperability/INTEROPERABILITY-LAYERS.md`
- ADR-003, ADR-008, ADR-011, ADR-015
