# Avaliação de prontidão — debate público e candidatura NGI

**Estado:** documento vivo. Serve para afinar continuamente o que falta; os
achados têm ID estável (`R*`) e não são eliminados, apenas mudam de estado.
**Data da primeira redação:** 2026-08-11
**Base:** commit `3fdea7d`
**Método:** leitura do repositório e execução das suites, não leitura apenas
declarativa. Distingue explicitamente **maturidade arquitetural** (o que o
repositório demonstra por si) de **evidência externa** (o que só terceiros
podem produzir).

**Pergunta que originou o documento:** *o que o formato NDF oferece e permite,
e está suficientemente desenvolvido para uma apresentação para debate e para
candidatura NGI?*

**Resposta curta:** o NDF está pronto em conteúdo técnico e sobredesenvolvido
face à demonstração. O que falta não é especificação — é evidência executável
e validação independente. As decisões da secção 1 reordenam o trabalho em
função disso.

---

## 1. Decisões de sequenciamento (2026-08-11)

Tomadas pelo responsável do projeto em resposta a esta avaliação. Alteram o
plano operacional anterior em [`../roadmap/NGI-MVP-2026.md`](../roadmap/NGI-MVP-2026.md).

### D1 — Debate público condicionado a renderização funcional

A discussão pública deixa de ter critério temporal (janela de datas) e passa a
ter critério de evidência: só se leva a debate uma especificação que se
demonstre a produzir artefactos reais.

**Formulação registada (versão desacoplada):**

- **`normordis-pdf` funcional é a condição de abertura** da revisão pública;
- **`normordis-odf` é evidência de segunda implementação**, posterior, e **não
  bloqueia** a abertura.

A formulação inicial exigia ambos os renderizadores. Foi desacoplada porque
`normordis-odf` não tem hoje repositório nem estimativa, e condicionar a
revisão a trabalho por dimensionar adiava o primeiro contacto externo por prazo
indeterminado — precisamente quando D5 congela o âmbito da especificação. Um
renderizador funcional já prova implementabilidade; o segundo prova
independência de caminho, que é uma afirmação distinta e pode chegar depois.

**Consequência imediata:** PR-001, registado em
[`../normalization/REVIEW-LOG.md`](../normalization/REVIEW-LOG.md) com janela
proposta 2026-07-01 → 2026-08-15 e estado `preparação`, **não abre nessa
janela**. Tem de ser explicitamente adiado no registo, com a nova condição de
abertura em vez de datas — ver `R1`. Enquanto isso não acontecer, o estado
comunicado no `README.md` ("Draft — Revisão pública") descreve algo que não
está a decorrer.

**Fundamentação:** abrir revisão pública sem renderizador funcional convida
comentários sobre o texto e não sobre o comportamento.

**Risco assumido e a vigiar:** D1 e D5 combinadas congelam o âmbito da
especificação *antes* de qualquer contacto externo. «Não falta nada a prever»
(D5) é exatamente o tipo de afirmação que só revisão externa consegue testar.
Se a revisão pública revelar lacunas de âmbito — e não apenas defeitos —, o
congelamento terá de ser reaberto. Regista-se aqui para que essa reabertura,
se ocorrer, seja lida como resultado esperado do processo e não como falha de
planeamento.

### D2 — Adapters XML despriorizados

O pacote `normordis-xml-adapters` (milestone M3 do plano NGI) **deixa de ser
crítico** e sai do caminho crítico da demonstração.

**Fundamentação do responsável:** o XML apenas reproduziria o payload de
dados, e o NDF não substitui os dados estruturados dos sistemas aplicacionais
— é coerente com o princípio de âmbito já fixado em [`../../LACUNAS.md`](../../LACUNAS.md).
Um adapter que só reserializa aquilo que a base de dados de negócio já detém
não demonstra a proposta de valor do formato; demonstra apenas conversão.

**Consequência:** a demonstração fim-a-fim passa a ser `NDF + NDT → PDF` —
e, mais tarde, `NDF + NDT → ODF` — sem etapa XML a montante. O trabalho de
adapters permanece legítimo como **trabalho futuro financiável** numa
candidatura, não como pré-requisito dela.

**Efeito colateral a assumir:** desaparece a única demonstração prevista de
*ingestão* de formatos institucionais existentes. Ver `R13`.

### D3 — Versão inglesa necessária

O conjunto passa a exigir uma versão em inglês. Hoje não existe um único
ficheiro `.en.md` no repositório e a avaliação externa — NGI ou normalização
CEN/ISO — não se faz em português. Ver `R3` para o âmbito mínimo.

### D4 — Fixtures CAdES reais entram no roadmap

O gate CAdES deixa de ser apenas "gate externo pendente" e passa a item de
roadmap com trabalho atribuível. Ver `R2`.

### D5 — NDF-core congelado em âmbito

O responsável confirma que o NDF **já prevê tudo o que foi idealizado** —
guarda de documentos, metadados de segurança, auditoria, relação com outros
documentos, intervenientes — e que não identifica nada em falta a prever.

**Consequência:** cessa o trabalho de alargamento normativo do NDF-core. As
alterações admissíveis passam a ser correções de defeito, clarificações
resultantes de revisão externa, e o trabalho editorial já previsto para
normalização (linguagem, termos e definições, anexos). O esforço de
desenvolvimento desloca-se para NDT, NCRTF, `normordis-pdf` e `normordis-odf`.

Itens já registados para versões futuras (1.1.0, 1.2.0, 2.0.0 em
[`../../ROADMAP.md`](../../ROADMAP.md)) mantêm-se como estão — são evolução
planeada, não lacunas do âmbito atual.

### D6 — Procura de necessidade institucional em linha paralela

A demonstração de necessidade por utilizadores institucionais (gate externo 7,
achado `R5`) passa a linha de trabalho **paralela**, não dependente de
renderizadores nem de qualquer marco de engenharia. É o gate externo com maior
peso numa candidatura de *digital commons*, o mais barato de perseguir, e o
único que nenhuma quantidade de código resolve.

### D7 — Eixos de posicionamento do NDF

O âmbito do NDF passa a ser comunicado por três eixos, aplicáveis tanto ao
debate como à candidatura:

**1. Soberania documental.** A entidade detém o documento em dados canónicos
próprios, não em bytes de página de um fornecedor. Sem aprisionamento a
formato, produto, linguagem, runtime ou base de dados.

**2. Eficiência e capacidade.** Não apenas espaço ocupado, mas o que o formato
permite fazer que uma representação de página não permite: consulta e
indexação de dados estruturados, validação por schema, ligação verificável a
outros documentos por hash, metadados de segurança e de avaliação arquivística
dentro dos bytes assinados, prova de integridade sem abrir o documento.

**3. Implementabilidade livre por terceiros.** Especificação CC0, schemas
legíveis por máquina, suite de conformidade executável, conformidade definida
por papel. Qualquer entidade ou fornecedor implementa sem dependência
contratual do NORMORDIS.

**Cautela normativa sobre o eixo 2 — a única afirmação frágil dos três.** Os
eixos 1 e 3 são verificáveis hoje, a partir do próprio repositório, sem
depender de gate externo. O eixo 2 não é: assenta em medição, e a medição atual
é de um único fixture (`R6`). A comparação depende inteiramente da unidade
escolhida — o NDF-core do ofício de exemplo são 3 377 bytes, mas o `.ndfpkg`
completo são 71 211 bytes, mais do que muitos PDF/A da mesma página. Afirmar
«o NDF ocupa menos espaço que o PDF» é refutável em debate com um único
contraexemplo.

O enquadramento defensável é o do **custo à escala e da capacidade**: milhares
de documentos partilham um NDT, os recursos deduplicam-se, e o que fica
armazenado é dado estruturado indexável em vez de bytes de página. Qualquer
alegação quantitativa exige o corpus comparativo previsto em `R6`, com a
unidade de comparação declarada.

---

## 2. O que o NDF oferece hoje — verificado

Verificado por execução, não por leitura das declarações do repositório:
`python3 tools/validate.py` → **58/58**.

| Capacidade | Referência normativa | Observação |
|---|---|---|
| Bytes canónicos JCS/RFC 8785 e `payload_hash` | SPEC §1.3, §2.5 | vetores cruzados Python **e** Node.js na CI, incluindo RFC 8785 Appendix B |
| Separação NDF-core (assinado) ↔ envelope (não assinado) | SPEC §1.2 | elimina a circularidade da assinatura sobre si própria |
| `validation_code` — SHA-256 + BASE32, 100 bits | SPEC §4.6 | verificável a partir do documento impresso; intrínseco ao formato, independente de serviço (ADR-010) |
| Grafo documental verificável `relacoes[]` | SPEC §2.11 | ligado ao `payload_hash` do alvo; 11 tipos fechados + extensão `ext.<entidade>.<tipo>` (ADR-008) |
| Sucessão documental dentro dos bytes assinados | SPEC §6, ADR-011 | `versao_anterior`/`hash_anterior` removidos do envelope |
| Avaliação arquivística PCA/destino final (MEG/DGLAB) | SPEC §3 | dentro do core, logo canonicalizada e assinada |
| Tombstone de eliminação | SPEC §2.4.3 | resolve imutabilidade ↔ RGPD art.º 17.º, especificado byte a byte |
| `proveniencia_ia` com estado de revisão humana | SPEC §2.13, ADR-005 | diferenciador relevante para discurso NGI e AI Act |
| Múltiplas assinaturas autocontidas | SPEC §4.4, ADR-004 | `assinatura_id`, `papel`, `ordem`, material de validação **por entrada** |
| `.ndfpkg` autocontido | SPEC §8 | 1 exemplo positivo + 8 vetores negativos de inventário/caminhos/envelope |
| Conformidade por papel | SPEC §9 | produtor, leitor, pacote; 54 IDs de requisito auto-gerados de **DEVE**/**NÃO DEVE** |
| Perfil de Ciclo de Vida separado da conformidade de formato | SPEC §9.5, ADR-010 | família `CUST-REQ-*` distinta de `NDF-*` |
| Separação dados / apresentação / texto rico | NDF + NDT + NCRTF | NDT é layout puro, sem lógica de negócio |

**Andaime de normalização já existente:** governação, política de versões,
política editorial, base terminológica, referências normativas, matriz de
rastreabilidade, registo IPR, registo de revisão pública, 11 ADRs, e guardrails
de CI que verificam coerência SPEC ↔ schemas ↔ exemplos
([`../../tools/check_spec_coherence.py`](../../tools/check_spec_coherence.py)).

Este último merece nota: nasceu da constatação, na Fase 1C, de que **58 testes
verdes não demonstravam coerência da especificação** — três blocos JSON da
própria SPEC eram inválidos contra schemas que a SPEC torna obrigatórios. A
lição está registada e mecanizada, não apenas anotada.

---

## 3. Fora de âmbito por desenho — e isso é uma força

Documentado em [`../../LACUNAS.md`](../../LACUNAS.md): workflow e estado
processual, notificação e entrega, validação de competência para estabelecer
relações, controlo de acesso e confidencialidade (SPEC §1.5), resolução de
identidade de participantes.

Dos dez pontos da revisão adversarial, dois foram **retirados** por estarem
fora de âmbito e um foi **fechado por decisão consciente de não alterar o
schema** (ADR-009). Num debate, isto é material a usar ativamente: demonstra
que o formato tem uma fronteira definida e defendida, não uma fronteira
acidental.

---

## 4. NDF face à abordagem tradicional — vantagens e desafios

«Abordagem tradicional» significa aqui o documento institucional como ficheiro
de página — PDF, DOCX/ODT ou papel digitalizado — com os metadados a viver
numa aplicação de gestão documental à parte.

Esta secção existe para o debate. Um argumentário só com vantagens é lido como
material promocional e perde credibilidade na primeira pergunta difícil; os
desafios abaixo devem ser apresentados por iniciativa própria, não arrancados
por um revisor.

### 4.1 Vantagens

| # | Vantagem | Face ao tradicional |
|---|---|---|
| V1 | **Fonte de verdade em dados** | Consulta, indexação, agregação e reutilização diretas. No tradicional, extrair informação de um PDF exige OCR ou heurísticas sobre layout — frágeis e não auditáveis |
| V2 | **Integridade verificável sem abrir o documento** | `payload_hash` sobre bytes canónicos JCS. No tradicional, verificar exige abrir o ficheiro e confiar no visualizador para relatar corretamente o estado da assinatura |
| V3 | **Metadados dentro dos bytes assinados** | Classificação de segurança, base legal RGPD e entidade produtora são canonicalizados e assinados. No tradicional, os metadados vivem fora do ficheiro (na aplicação) ou em XMP alterável, e perdem-se na exportação ou migração de sistema |
| V4 | **Avaliação arquivística nativa** | PCA e destino final (MEG/DGLAB) dentro do próprio documento (SPEC §3). No tradicional é atributo de uma tabela da aplicação — quando o sistema é substituído, tipicamente perde-se |
| V5 | **Relações entre documentos verificáveis** | `relacoes[]` liga ao `payload_hash` exato do alvo. No tradicional a relação é texto — «na sequência do ofício n.º X» — não verificável por máquina e não resistente a substituição do alvo |
| V6 | **Eliminação seletiva compatível com RGPD** | Tombstone especificado byte a byte (SPEC §2.4.3). Num PDF assinado, apagar dados pessoais destrói a assinatura; o NDF define o que se destrói e o que subsiste como prova |
| V7 | **Apresentação separada dos dados** | Alterar norma gráfica ou identidade visual não obriga a regerar nem a reassinar documentos: troca-se o NDT. O mesmo NDF-core renderiza para PDF, ODF ou HTML |
| V8 | **Proveniência de IA estruturada** | `proveniencia_ia` com estado de revisão humana obrigatório por intervenção. Não existe equivalente no fluxo tradicional |
| V9 | **Deduplicação à escala** | Milhares de documentos partilham um NDT e os recursos deduplicam-se. É aqui — e não no documento isolado — que a eficiência de armazenamento se materializa |
| V10 | **Acessibilidade derivada da semântica** | A estrutura lógica está nos dados, logo a saída PDF/UA-2 é gerada a partir dela. No tradicional, a acessibilidade é remendada depois, sobre um artefacto que já perdeu a estrutura |
| V11 | **Independência de fornecedor, verificável hoje** | Especificação CC0, schemas legíveis por máquina, suite de conformidade executável, conformidade definida por papel. Não depende de gate externo nenhum para ser demonstrada |
| V12 | **Código de verificação para o cidadão** | `validation_code` de 100 bits impresso no documento, verificável por quem o recebe. No tradicional, a verificação exige software de assinatura e literacia técnica |

### 4.2 Desafios

| # | Desafio | Gravidade e mitigação |
|---|---|---|
| C1 | **Não é legível por humanos sem renderizador.** Um PDF abre em qualquer máquina, hoje e provavelmente daqui a trinta anos. Um NDF sem NDT e sem renderizador é JSON | **O contra-argumento mais forte do lado tradicional, e o mais legítimo.** Mitigação: o `.ndfpkg` transporta o NDT e os schemas, tornando-se autocontido; e a saída PDF/A continua a ser produzida como representação visual preservável. Mas a mitigação é *acrescentar um PDF*, não dispensá-lo — o que deve ser dito com franqueza |
| C2 | **Determinismo do renderizador** (*what you see is what you sign*) — reformulado, ver 4.2.1 | Não é «assina-se algo que não se viu»: `ndt_version_ref` é campo obrigatório do NDF-core, logo a assinatura vincula **dados + versão exata do template**, e o produtor mostra a renderização antes de assinar. O que fica por vincular é o **renderizador**: dois renderizadores conformes podem divergir em paginação, quebra de linha ou substituição de fontes. Gate de implementação já identificado em `specs/ndt/RENDERER-CONFORMANCE.md` (testes golden em falta), não defeito do modelo de assinatura. Para casos que exijam vincular o artefacto visual, existe o modo híbrido CAdES+PAdES |
| C3 | **Ecossistema inexistente** | Nenhum sistema de gestão documental comercial lê NDF. Toda a adoção exige trabalho de integração, suportado pelo adotante. Os schemas e a suite de conformidade reduzem o custo; não o eliminam |
| C4 | **Exige que a entidade já tenha os dados estruturados** | Uma entidade cujo processo termina num documento escrito à mão em Word não retira benefício imediato — teria primeiro de estruturar a produção documental. O NDF é mais fácil de adotar a jusante de sistemas aplicacionais do que a jusante de processos manuais |
| C5 | **Sem estatuto normativo** | O PDF/A é ISO 19005 desde 2005 e é aceite por arquivos nacionais como formato de preservação. O NDF é um draft de projeto. Um arquivo pode recusá-lo por esse motivo isolado, independentemente do mérito técnico — e tem fundamento para o fazer |
| C6 | **Dependência do par NDF+NDT para reconstituição fiel** | Preservar o NDF sem o NDT correspondente degrada a reconstituição. O `.ndfpkg` e `ndt_version_ref` mitigam, mas transferem para a entidade uma disciplina de preservação que o ficheiro de página não exigia |
| C7 | **Acoplamento do bloco `avaliacao` ao modelo arquivístico português** | Barreira direta à adoção fora de Portugal e ponto sensível numa candidatura de âmbito europeu. Registado como `R11` e como nota para v2.0.0 |
| C8 | **Longevidade da cadeia criptográfica** | SHA-256 e as cadeias de certificados envelhecem. O CAdES-B-LTA e a re-selagem periódica (T6, Fase 5) são a resposta prevista, mas implicam infraestrutura viva ao longo de décadas — algo que um PDF/A em prateleira não exige |
| C9 | **Alegação de eficiência refutável se mal enquadrada** | Ver D7. O `.ndfpkg` de exemplo tem 71 211 bytes contra 3 377 do NDF-core isolado; escolher mal a unidade de comparação entrega o argumento ao interlocutor |
| C10 | **Complexidade acrescida no produtor** | Canonicalização JCS, pipeline de finalização de ordem estrita (SPEC §5.2), gestão de envelope e de custódia. Produzir um PDF é incomparavelmente mais simples. A complexidade paga-se em verificabilidade e em capacidade — mas é uma troca, não um ganho puro |

### 4.2.1 Nota sobre C2 — *what you see is what you sign*

Registada porque a formulação inicial deste desafio estava sobredimensionada e
a versão corrigida é material útil para o debate.

**Formulação inicial (incorreta por omissão):** «quem assina um NDF assina
bytes canónicos, não a página que viu».

**Correção.** Dois factos alteram o quadro:

1. **`ndt_version_ref` é campo obrigatório de topo do NDF-core** (SPEC §2.2).
   Está dentro dos bytes canonicalizados e assinados. A assinatura vincula,
   portanto, **dados + versão exata do template** — não apenas dados.
2. **A confirmação visual acontece no produtor, antes de assinar.** Recolhida
   uma declaração num formulário, ou produzido um ofício numa interface, o
   documento é visualizado e confirmado; só então é assinado. É exatamente o
   que sucede hoje, em que um documento só se converte em PDF depois de os
   dados estarem confirmados.

Face ao fluxo tradicional, o NDF fica **melhor** neste ponto, não pior: hoje
nada vincula os dados ao modelo usado para os apresentar — o template é um
ficheiro no disco de alguém, substituível sem deixar rasto. No NDF, a
identidade da versão do template está dentro da assinatura.

**O que sobra, e é real:** o **renderizador** não é vinculado. Dois
renderizadores conformes podem divergir em paginação, quebra de linha ou
substituição de fontes a partir do mesmo NDF+NDT.

Isto não é defeito do modelo de assinatura do NDF — é um gate de implementação
do NDT, já identificado em
[`../../specs/ndt/RENDERER-CONFORMANCE.md`](../../specs/ndt/RENDERER-CONFORMANCE.md):
o perfil de layout fixo exige testes golden sobre número e caixas de páginas,
*bounding boxes* com tolerância declarada, identidade de fontes e recursos
incorporados — e o documento reconhece que os resultados golden ainda não
existem no repositório. É também aqui que `normordis-odf`, enquanto segunda
implementação, produzirá a primeira evidência a sério.

Para os casos em que o artefacto visual tenha de ser vinculado — e não apenas
os dados que o geram — existe o modo híbrido CAdES+PAdES do NDT, que assina
também o PDF.

**Como responder em debate:** «a assinatura cobre os dados e a versão do
template, ambos dentro dos bytes assinados; a fidelidade da renderização é
garantida por perfil de conformidade de renderizador com testes golden, e o
PDF pode ser adicionalmente assinado com PAdES quando o caso o exigir.»

### 4.3 Como usar isto em debate

A posição defensável **não** é «o NDF substitui o PDF». É:

> O NDF é a forma de **guardar** o documento; o PDF/A continua a ser a forma de
> o **mostrar e preservar visualmente**. O erro do modelo tradicional não é usar
> PDF — é usar o PDF como *fonte de verdade*, guardando bytes de página e
> deixando os metadados, a avaliação arquivística e as relações documentais
> dependentes de uma aplicação que será substituída antes do documento
> prescrever.

Assim enquadrado, C1 e C5 deixam de ser objeções e passam a ser parte do
desenho: o PDF/A é produzido, preservado e assinado — só não é onde a verdade
reside.

**Formulação mais curta, do ponto de vista de quem decide:**

> Ao guardar um NDF, o software produtor está a optar por guardar o documento
> num formato reprodutível e com os metadados que o acompanham, em vez de
> simplesmente emitir um documento impresso e deitar fora tudo o resto.

Esta é a forma mais económica de expor a tese, porque desloca o debate do
terreno errado — «que formato é melhor?» — para o terreno certo: **o que se
perde no momento da emissão**. No fluxo tradicional, no instante em que o
documento se torna uma página, perdem-se os dados estruturados, a ligação
verificável aos documentos relacionados, a classificação de segurança e a
avaliação arquivística — ou melhor, passam a depender de uma aplicação que
será substituída muito antes de o documento prescrever. O NDF não acrescenta
um formato; **retém o que o modelo tradicional descarta**.

Corolário útil: a pergunta a fazer a uma entidade não é «quer adotar o NDF?»,
mas «quando emite um ofício, onde ficam os metadados, e o que lhes acontece
quando mudar de sistema?».

---

## 5. Achados — o que falta

Estado: `aberto`, `em curso`, `fechado por decisão`, `resolvido`.

| ID | Achado | Impacto | Estado |
|---|---|---|---|
| R1 | PR-001 registado com janela 2026-07-01 → 2026-08-15 e estado `preparação`, sem commit fixado e com zero comentários. A janela expira sem que a revisão tenha aberto, enquanto o `README.md` e as seis SPECs comunicavam "Draft — Revisão pública" | Alto — insustentável em debate; é a primeira coisa que um revisor competente verifica | **resolvido** (2026-08-11) — ver abaixo |
| R2 | Gate CAdES sem qualquer evidência: `tools/check_cades_gate.py` reporta **12/12 fixtures em `skeleton`** (5 positivas, 7 negativas). A alegação de valor probatório de longo prazo — o argumento mais forte do formato — não tem hoje um único byte de suporte | Alto — pergunta inevitável em debate e em avaliação | **aberto** — promovido a item de roadmap por D4 |
| R3 | Nenhum ficheiro `.en.md` no repositório. O único texto em inglês é a mensagem curta de §11 do plano NGI | Alto para avaliação externa; bloqueante para normalização CEN/ISO | **aberto** — aceite por D3 |
| R4 | Nenhuma implementação independente. `normordis-pdf` é do mesmo autor — não constitui validação cruzada (gate externo 6) | Alto — é o critério que mais pesa numa candidatura de commons digitais | **aberto** — `normordis-odf` (R9) mitiga parcialmente, mas continua a ser o mesmo autor |
| R5 | Nenhuma necessidade manifestada por utilizador institucional (gate externo 7). Registo IPR sem declarações | Médio-alto — "quem precisa disto?" sem resposta documentada | **em curso** — promovido a linha paralela por D6 |
| R6 | Eficiência de armazenamento é objetivo declarado em SPEC §1.1 e está sustentada por **uma** medição de um fixture ([`../../benchmarks/results/oficio-package.json`](../../benchmarks/results/oficio-package.json)) | Alto — deixa de ser lacuna de evidência e passa a risco de refutação direta, por D7 fazer da eficiência um eixo de comunicação | **em curso** — corpus comparativo NDF+NDT / PDF-A / ODT, a 1 e a N documentos, com unidade declarada |
| R7 | Portal de verificação existe apenas como contrato OpenAPI. O `validation_code` é a funcionalidade mais comunicável a não-técnicos e não tem implementação | Médio — afeta a demonstração, não a especificação | **aberto** |
| R8 | `normordis-pdf` **não renderiza NDT 2.0.0**: `render_template()` é um stub que devolve erro. O que renderiza é o modelo legado `body`+`{{placeholders}}`. Ver 5.1 | Alto — é agora, por D1, **a** condição de abertura do debate, e o esforço é muito superior ao estimado | **aberto** — reestimado em 2026-08-11 |
| R14 | Colisão de nomes: o `NdfDocument` de `normordis-pdf` (`NDF_VERSION = "1.1.0"`, documentado como «NORMAXIS Document Format») é um **formato diferente** do NDF-core da especificação (1.0.0), sem um único campo em comum. O crate está publicado no crates.io | Alto — dois formatos incompatíveis com o mesmo nome, um deles distribuído pelo próprio projeto. Indefensável num debate público | **resolvido** (2026-08-11) — ver 5.3 |
| R15 | `Campo.referencia` (caminho para `NDF-core.documento`, mecanismo normativo de ligação de dados em NDT §campos) é desserializado no modelo mas **nunca lido** por nenhum componente de renderização. A ligação de dados efetiva é `{{placeholder}}` contra um mapa plano | Alto — é a junta entre NDF e NDT; sem ela não há fluxo NDF+NDT→PDF | **aberto** |
| R9 | `normordis-odf` não existe: sem repositório, sem perfil mínimo definido, sem estimativa | Médio — evidência de segunda implementação; **não bloqueia** a abertura do debate, por D1 desacoplada | **aberto** |
| R10 | `normordis-xml-adapters` não existe (milestone M3 do plano NGI, prazo 2026-08-31) | — | **fechado por decisão** (D2) |
| R11 | O bloco `avaliacao` continua semanticamente acoplado ao modelo arquivístico português (PCA, DF, Lista Consolidada, DGLAB). Aceitável para 1.0 focada na AP portuguesa; relevante se o âmbito da candidatura for europeu | Médio — já registado em [`../../ROADMAP.md`](../../ROADMAP.md) como nota para v2.0.0, sem ação prevista | **aberto, sem ação** |
| R12 | O plano em [`../roadmap/NGI-MVP-2026.md`](../roadmap/NGI-MVP-2026.md) ficou desatualizado: M2 (2026-08-15), M3 (2026-08-31), M4 (2026-09-15) e M5 (2026-09-30) assentam numa cadeia sequencial que D1 e D2 alteram | Médio — documento de orientação a induzir em erro se não for anotado | **em curso** — anotado como parcialmente superado |
| R13 | A tese escrita em `NGI-MVP-2026.md` §2 e §11 é de *interoperabilidade documental*, mas a evidência demonstrável passa a ser saída para dois formatos. Reformulado em 2026-08-11: o problema **não** é a ausência do adapter XML — é a confusão de camadas na própria tese. Ver 5.2 | Médio-alto — desalinhamento entre a tese comunicada e a evidência demonstrável | **resolvido** (2026-08-11) — nota informativa `docs/interoperability/INTEROPERABILITY-LAYERS.md`; a interoperabilidade a demonstrar é ao nível do **pacote documental** (depósito OAIS), não dos dados |

---

### 5.1 R8 — reestimativa de `normordis-pdf` (2026-08-11)

Análise do repositório `normordis-pdf` no commit `c591385` (último de
2026-07-16). O crate compila (`cargo check --all-targets` limpo, apenas
avisos).

**Achado central: o renderizador NDT 2.0.0 não existe.** Não é uma lacuna
parcial — é um stub explícito:

```rust
/// NDT 2.0.0 render entry point (positioned-layout renderer not yet implemented).
pub fn render_template(_doc, _data, _style) -> Result<Vec<Box<dyn Element>>, TemplateError> {
    Err(TemplateError::RenderError(
        "NDT 2.0.0 positioned-layout renderer not yet implemented".into(),
    ))
}
```

O que o crate renderiza hoje é o modelo **legado** `model::legacy_body::BodyElement`
— um array `body` com `{{placeholders}}`, correspondente aos seus próprios
templates de exemplo, que declaram `"ndt": "1.0.0"` com `meta`/`placeholders`/`body`.

**Estado por construção NDT 2.0.0:**

| Construção | Modelo (`model.rs`) | Renderização |
|---|---|---|
| `paginas_def`, `sequencia` | ✅ desserializa | ❌ não consumida na renderização |
| `campos[]` | ✅ desserializa | ❌ `Campo`/`campos` não aparece em nenhum módulo fora de `model.rs` |
| `graficos[]` (11 primitivas) | ✅ desserializa | ❌ nenhuma renderizada |
| `blocos[]` (tabela, corpo, cabeçalho, rodapé) | ✅ desserializa | ❌ nenhum renderizado |
| `fluxo` | ✅ desserializa | ❌ não renderizado |
| `incluir_se` | ✅ desserializa | ❌ não avaliado |

**Atenuante importante:** as primitivas de baixo nível existem e estão
testadas. `fixed_text`, `fixed_line`, `fixed_image`, `FixedBox` com política de
overflow, `Table`, motor de linha Knuth-Plass, `richtext` (NCRTF), fontes
incorporadas, PDF/A (`src/compliance/`), PDF/UA (`src/compliance/ua.rs`),
assinatura e TSA. O trabalho é de **ligação**, não de raiz.

**O que falta mesmo construir de novo**, cruzando as primitivas usadas pelos
NDT de exemplo com o que existe no crate:

| Primitiva | Usada em | Existe base? |
|---|---|---|
| `texto_fixo` | Rosto ×60, Anexo A ×19 | ✅ `fixed_text` |
| `rectangulo` | Rosto ×46, Anexo A ×7 | ✅ primitiva `rect_` no backend |
| `linha` | Rosto ×9, Anexo A ×6, ofício ×2 | ✅ `fixed_line` |
| `imagem` | ofício ×2 | ✅ `fixed_image` |
| bloco `tabela` | Rosto ×1, Anexo A ×2 | ✅ `Table` |
| **`grelha_digitos`** | Rosto ×5, Anexo A ×3 | ❌ **ausente** |
| **`codigo_barras`** | Rosto ×2, Anexo A ×1, ofício ×1 | ❌ **ausente** |
| **`fluxo`** | ofício (2 páginas) | ⚠️ existe `page_flow` genérico, sem o modelo NDT (`linha_lateral`, `quebra_pagina`) |
| `poligono`, `elipse`, `svg`, `tabela_visual`, `assinatura` | não usadas nos exemplos | ❌ ausentes — **não bloqueiam o Modelo 3** |

**Consequência para a estimativa.** «Alinhar `normordis-pdf` ao caso Modelo 3»
não é ligar um caso de teste: é implementar o renderizador de layout
posicionado do NDT 2.0.0. Para o caso Modelo 3 Rosto + Anexo A, o âmbito
mínimo é: percurso `paginas_def`/`sequencia`, resolução de `campos[]`,
quatro primitivas gráficas sobre bases existentes, duas primitivas novas
(`grelha_digitos`, `codigo_barras`), o bloco `tabela` e a avaliação de
`incluir_se`. O `fluxo` só é necessário para o ofício, não para o Modelo 3 —
o que sugere fazer o Modelo 3 primeiro.

**Dois achados adicionais, de natureza diferente e mais incómodos:**

**R14 — colisão de nomes.** O `NdfDocument` do crate declara
`NDF_VERSION = "1.1.0"` e está documentado como «NORMAXIS Document Format»,
com os campos `ndf`, `origin`, `revision`, `meta`, `output`, `styles`,
`content`, `integrity`, `audit`, `outputs`, `signatures`, `page`,
`embedded_fonts`. O NDF-core da especificação é 1.0.0 e tem `ndf_version`,
`ndf_id`, `estado`, `payload_hash_alg`, `nivel_assinatura`, `ndt_version_ref`,
`metadados`, `documento`, `avaliacao`. **Não partilham um único campo.** São
dois formatos diferentes com o mesmo nome, e o crate está publicado no
crates.io. Igualmente, `ndt-tools` descreve NDT como «NORMAXIS Document
Template». Isto tem de ser resolvido — por renomeação do lado do crate ou por
alinhamento — antes de qualquer apresentação pública, sob pena de a primeira
pergunta do debate ser «então afinal o que é o NDF?».

**R15 — a junta NDF↔NDT não está implementada.** `Campo.referencia` é o
mecanismo normativo de ligação de dados: um caminho relativo a
`NDF-core.documento` (por exemplo `identificacao.primeira_entrega`,
`quadro3.totais_a.rend_bruto` nos exemplos Modelo 3). No crate, `referencia` é
desserializado e nunca lido; a ligação efetiva faz-se por `{{placeholder}}`
contra um `HashMap` plano em `NdtData`. Enquanto isto não mudar, **não existe
caminho de NDF-core para PDF** — existe caminho de dados avulsos para PDF.

---

### 5.2 R13 — camada de dados vs. camada de documento (2026-08-11)

Reformulação do achado, na sequência da observação do responsável de que **o
NDF não é um formato de dados, é um formato de documento**.

**A observação está correta e é decisiva.** Os formatos XML institucionais
correntes — SAF-T PT, Modelo 3, formatos de faturação — são contratos de
**intercâmbio de dados**: transportam o dado de negócio que vive nos sistemas
aplicacionais. O NDF opera noutra camada: transporta o **documento
finalizado** — imutável, assinado, com metadados, avaliação arquivística,
relações e intervenientes.

Um adapter XML↔NDF conflaciona as duas camadas:

- **XML → NDF** seria «construir um documento a partir de dados» — mas é
  exatamente o que a aplicação produtora já faz, a partir dos seus próprios
  dados. O adapter não acrescenta capacidade; acrescenta um desvio.
- **NDF → XML** seria «voltar a extrair os dados» — descartando precisamente
  aquilo que faz do NDF um documento (assinatura, custódia, avaliação) e
  devolvendo dados que o sistema de origem já tinha.

Isto **reforça D2 para além da fundamentação original**: o adapter XML não é
apenas não-crítico, é conceptualmente mal colocado. Não deve ser reposto no
roadmap.

**Mas a interoperabilidade não desaparece — muda de camada.** Existem
contratos XML que operam ao nível do **documento e do pacote**, não dos dados,
e esses estão na mesma camada que o NDF:

| Contrato | Camada | Relevância |
|---|---|---|
| OAIS / METS / PREMIS (SIP de depósito) | pacote documental + metadados de preservação e fixidez | Depósito em arquivo definitivo. O NDF declara em SPEC §1.1 o apoio à gestão arquivística e refere ISO 15489-1 e MoReq2017 — que implicam interfaces de depósito |
| ETSI ASiC (contentor assinado) | pacote assinado | Ocupa espaço comparável ao `.ndfpkg`; comparação relevante em contexto eIDAS |
| EAD | descrição arquivística | Relevante para a relação com o catálogo do arquivo |

**Consequência prática.** A pergunta de interoperabilidade que interessa não é
«como converto SAF-T em NDF?» — é **«como é que um `.ndfpkg` é depositado num
arquivo conforme OAIS?»**. Esta segunda pergunta está por responder, é a que
um arquivista competente fará (gate externo 3), e liga-se diretamente a `R5`:
é também a pergunta que abre a conversa com a DGLAB.

**Resolvido (2026-08-11)** com nota informativa, sem alteração à
especificação — compatível com D5:
[`../interoperability/INTEROPERABILITY-LAYERS.md`](../interoperability/INTEROPERABILITY-LAYERS.md).
Declara a posição por camadas, mostra que a ponte com sistemas XML de dados se
faz por **referência** (`ndf_id`/`payload_hash`) e não por conversão, e
identifica o depósito arquivístico conforme OAIS como a interoperabilidade a
demonstrar. Inclui a tabela dos pontos de contacto que **já existem** no
formato (fixidez, proveniência, retenção, relações), confirmando que o
trabalho futuro é de mapeamento e evidência, não de acrescento ao NDF.

---

### 5.3 R14 — resolução, e arquitetura em camadas de `normordis-pdf` (2026-08-11)

**Questão de fundo colocada pelo responsável:** `normordis-pdf` nasceu como
`normaxis-pdf` e pode querer manter-se como **renderizador PDF/UA autónomo**,
servindo simultaneamente o caminho NDF+NDT→PDF. É possível?

**Sim, e é a arquitetura correta.** O conflito não estava no crate querer os
dois papéis — estava em ter um tipo de camada baixa com nome de camada alta.

```text
Camada 1 — motor autónomo
  modelo de documento, layout, PDF/A, PDF/UA, fontes, NCRTF, assinatura, TSA
  → utilizável por quem nunca ouviu falar de NDF; é o que sustenta o crate
    como artefacto reutilizável e independente
        ▲
Camada 1.5 — arquivo de render (`RenderArchive`)
  proveniência do template, dados resolvidos, estilos, integridade, cadeia de
  auditoria, saídas, assinaturas, fontes embebidas
        ▲
Camada 2 — conformidade NDF/NDT
  consome NDF-core 1.0.0 + NDT 2.0.0 da especificação, resolve
  `campos[].referencia` contra `documento`, mapeia para a camada 1
  → é aqui que vive R15, e é o que falta construir
```

A camada 2 deve ficar atrás de uma *feature* Cargo, para o motor continuar
leve para quem só quer gerar PDF institucional.

**Rename executado** no repositório `normordis-pdf` (branch `devel`, sem
commit). O que era chamado NDF na crate é, de facto, um arquivo de render
autocontido — camada 1.5, não camada 2:

| Antes | Depois |
|---|---|
| `NdfDocument` | `RenderArchive` |
| módulo `ndf` | módulo `archive` |
| `template::ndf_pipeline` | `template::archive_pipeline` |
| `NdfOrigin`, `NdfMeta`, `NdfIntegrity`, `NdfAudit`, `NdfOutput`, `NdfSignature`, `NdfEmbeddedFont`, `NdfRevision`, `NdfRecord*`, `NdfRegistry`, `NdfFilter` | prefixo `Archive*` |
| `parse_ndf`, `verify_ndf`, `render_ndf`, `render_ndf_with_fonts`, `render_ndf_prepared_for_signing[_with_fonts]` | `*_archive` |
| `NDF_VERSION` | `ARCHIVE_VERSION` (valor inalterado) |
| `Ndf*Error` | `Archive*Error` |
| campo serializado `ndf` | `archive`, com `alias = "ndf"` |
| evento `signature.ndf.applied` | `signature.archive.applied`, com alias |

Os *aliases* de serde garantem que arquivos escritos por versões anteriores
continuam a ser lidos — a rutura é de API, não de dados.

**Mantido deliberadamente:** `CampoNdf` / `campo_ndf`. É construção do NDT
2.0.0 (`specs/ndt/schemas/ndt.schema.json`) e refere-se legitimamente ao NDF
da especificação.

**Também corrigido (R14b):** rótulos de proprietário errados — NCRTF, NDT e
NDF são formatos NORMORDIS, e apareciam documentados como NORMAXIS em
`src/lib.rs`, `tools/ndt-tools` e `tools/dotx2ndt`. As menções ao *framework*
NORMAXIS, que são legítimas, mantiveram-se. A versão do NDT na documentação do
crate estava em `v1.3.0` e foi corrigida para `v2.0.0`, alinhando com
`ENGINE_NDT_VERSION`.

**Versão:** `3.0.0` → `4.0.0`, por alteração incompatível da API pública.
Publicação no crates.io fica a critério do responsável.

**Verificado:** `cargo check --all-targets` sem erros (apenas os três avisos
pré-existentes); `cargo test` **471 testes, 0 falhas**.

---

### R1 — resolução (2026-08-11)

| Alteração | Ficheiro |
|---|---|
| PR-001 passa a estado `adiado`; datas substituídas pela condição de abertura de D1; registado o que fica por fixar na abertura (commit, datas efetivas, canais) | [`../normalization/REVIEW-LOG.md`](../normalization/REVIEW-LOG.md) |
| Estado editorial corrigido de "Draft — Revisão pública" (nível 2) para "Draft — revisão pública por abrir" (nível 1) | `specs/ndf/SPEC.md`, `specs/ndt/SPEC.md`, `specs/ncrtf/SPEC.md`, `specs/registry/SPEC.md`, `specs/portal/SPEC.md`, `specs/ndt/RENDERER-CONFORMANCE.md` |
| Secção "Estado" reescrita: declara explicitamente que nenhum período de revisão está aberto e que nenhum dos oito gates externos está cumprido | [`../../README.md`](../../README.md) |
| Gate editorial passa a aceitar um conjunto de estados admissíveis, em vez de exigir literalmente o estado incorreto | [`../../tools/check_publication_profile.py`](../../tools/check_publication_profile.py) |

O último ponto era necessário: a ferramenta exigia a string `Draft — Revisão
pública` nas três SPECs, o que tornava o estado incorreto **obrigatório por
CI**. Passa a validar contra `ALLOWED_STATES`, mantendo-se como gate real —
continua a falhar se nenhum estado admissível for declarado.

Verificado após as alterações: `validate.py` 58/58, `check_publication_profile.py`
PASS, `check_spec_coherence.py` PASS, `audit_normative.py` PASS (54 IDs, 186
declarações), `build_review_bundle.py` PASS (213 ficheiros).

---

## 6. Gates externos — estado

Nenhum dos 8 gates de [`../normalization/READINESS.md`](../normalization/READINESS.md)
está cumprido. Isto não é defeito do trabalho feito: por definição, nenhum
deles pode ser cumprido por revisão interna. Regista-se aqui para que a
distinção fique explícita em qualquer apresentação.

| Gate | Depende de | Achado associado |
|---|---|---|
| 1. Fixtures CAdES-B-LTA reais | certificado/TSA de teste ou parceria | R2 |
| 2. Revisão criptográfica independente | especialista externo | — |
| 3. Revisão arquivística | especialista competente | R11 |
| 4. Revisão jurídica PT/eIDAS | jurista | — |
| 5. Revisão de acessibilidade | auditoria dos perfis de saída | R8, R9 |
| 6. Implementação/piloto independente | terceiro sem acesso ao código do produtor | R4 |
| 7. Necessidade institucional documentada | utilizador institucional | R5 |
| 8. Comissão Técnica NP/CEN/ISO | IPQ | — |

---

## 7. Sequência de trabalho resultante

Ordem derivada das decisões, não das datas do plano anterior.

**Caminho crítico — até à abertura do debate**

1. ~~**Corrigir o estado comunicado**~~ — ✅ **concluído em 2026-08-11** (R1).
2. **`normordis-pdf` até ao caso Modelo 3 fim-a-fim**, reproduzível a partir do
   README por alguém externo (R8). É a condição de abertura fixada por D1.
3. **Fixtures CAdES**, começando por um par mínimo: uma positiva com
   certificado de teste próprio e uma `payload-tampered` (R2). Converte um gate
   "pendente" num gate "iniciado com evidência".
4. **Versão inglesa** — `README.en.md` e abstract/âmbito das três SPECs primeiro;
   tradução integral depois, com a base terminológica bilingue já prevista (R3).

**Linhas paralelas — sem dependência do caminho crítico**

5. **Procura de necessidade institucional** (R5, D6). Não depende de
   engenharia; pode começar imediatamente.
6. **Corpus comparativo de eficiência e capacidade** (R6, D7) — NDF+NDT contra
   PDF/A e ODT, a 1 documento e a N documentos, com a unidade de comparação
   declarada. Requisito para qualquer afirmação quantitativa em debate.

**Posterior**

7. **`normordis-odf`** — definir primeiro o perfil mínimo (documento de texto
   sobre o modelo de fluxo do NDT → ODT), para o âmbito não crescer sem
   controlo (R9). Evidência de segunda implementação e resposta parcial a R4.
8. **Portal de verificação mínimo**, quando houver artefactos reais para
   verificar (R7).
9. **Decidir o enquadramento da tese** face à ausência de ingestão (R13).

Trabalho **não** nesta lista, por decisão: alargamento normativo do NDF-core
(D5) e adapters XML (D2).

---

## 8. Registo de verificação

Executado em 2026-08-11 sobre o commit `3fdea7d`, árvore limpa:

| Verificação | Resultado |
|---|---|
| `python3 tools/validate.py` | 58/58 |
| `python3 tools/check_cades_gate.py` | 12 casos pendentes, `fixture_state=skeleton` |
| Ficheiros `*.en.md` no repositório | 0 |
| Resultados de benchmark | 1 ficheiro |
| Repositório `normordis-xml-adapters` | inexistente |
| Repositório `normordis-odf` | inexistente |
| `normordis-pdf` — referências a Modelo 3 | nenhuma em código ou testes |
| `normordis-pdf` — último commit | 2026-07-16 |
