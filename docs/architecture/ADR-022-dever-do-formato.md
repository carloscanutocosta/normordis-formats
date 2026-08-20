# ADR-022: Dever do formato e responsabilidade do produtor

**Estado**: Aceite
**Data**: 2026-08-20
**Decisores**: carloscanutocosta

---

## Contexto

Ao abrir o NDF à captura de documentos produzidos fora do editor estruturado
(ADR-020), a tentação de o formato «melhorar» o que recebe aumenta: validar,
normalizar, completar, corrigir, recusar. É preciso um critério explícito, sob
pena de a fronteira se deslocar sozinha, uma cláusula de cada vez.

O projeto tem doutrina dispersa sobre isto — SPEC §1.1 declara que a validade
jurídica «não é garantida pelo formato isoladamente»; §1.4 e §2.13.1 dizem o
mesmo quanto a RGPD e AI Act; [`LACUNAS.md`](../../LACUNAS.md) L1 regista que
`relacoes[]` prova integridade e não legitimidade; o `README.md` remete
alegações jurídicas para avaliação competente. Falta a formulação positiva:
não o que o formato não garante, mas **o que lhe compete**.

O [`ROADMAP.md`](../../ROADMAP.md) tem, desde 2026-08-15, um teste que decide o
que **não entra** no NDF-core. Não tinha critério para o que **tem de ser
possível**.

## Decisão

**O formato deve permitir que toda a informação relevante e necessária possa
ser guardada e reproduzida. É esse o seu dever, e é só esse.**

Daqui saem duas obrigações simétricas:

| | Dever de quem |
|---|---|
| **Capacidade de representação** — existir lugar para tudo o que é relevante e necessário | **do formato** |
| **Correção do que se representa** — que o declarado seja verdadeiro, competente, completo e legal | **do produtor** |

Se algo relevante não tem onde ser guardado, é lacuna do formato e resolve-se no
formato. Se tem lugar e vem mal preenchido, não é problema do formato.

**Fidelidade ao emitido.** O sistema não corrige, não normaliza, não completa e
não reescreve. Já era regra para binário assinado externamente e para
`payload_bytes` (SPEC §5.3); passa a ser regra geral da captura. Uma deficiência
detetada regista-se; não se emenda.

**O teste operacional:** *um verificador consegue decidir isto tendo apenas o
pacote em mãos?*

| Pode ser requisito do formato | Não pode |
|---|---|
| **Estrutural** — o campo existe e tem esta forma | Que o valor declarado seja **verdadeiro** |
| **Consistência interna** — o hash bate com os bytes, `ndt_version_ref` resolve, `componentes[].sha256` bate com o inventário | Que o signatário tivesse **competência** para o ato |
| **Semântico-declarativo** — este campo significa isto, não inferir além disso | Que a classificação atribuída seja a **correta** |
| **Comportamento de leitor** — não renderizar um capturado aplicando o NDT a `documento` | Que estejam presentes **todos os anexos** que a lei exige |

Se a decisão exige o mundo — a lei, a orgânica, o procedimento, os factos — é do
produtor. Se se decide dentro do artefacto, pode ser conformidade.

## Alternativas consideradas

### O formato impõe completude jurídica

Impossível e mal colocado. Exigiria que o formato conhecesse a orgânica, as
competências delegadas, os requisitos legais de cada tipo de ato e a sua
evolução no tempo. Um formato que tentasse fazê-lo ficaria errado à primeira
alteração legislativa, e todos os documentos já assinados ficariam presos a uma
regra caduca.

### O formato cala-se sobre a fronteira

É o estado anterior a este ADR. Produz deslize: cada cláusula nova parece
razoável isoladamente, e o conjunto acaba por alegar mais do que pode sustentar.

## Justificação da decisão

O paralelo com o papel é exato e decide a questão. Um documento em papel pode
ser assinado por quem não tem competência: **o ato existe**, produz efeitos, e a
sua validade é decidida pelas autoridades próprias, administrativas e
judiciais. O suporte nunca decidiu isso — nem o papel, nem o NDF.

O que muda a favor do NDF é o que fica disponível para essa decisão posterior.
Quando a autoridade anula, a anulação é ela própria um documento, ligado ao
original por `relacoes[{tipo: "anula"}]`, e **o original é preservado intacto**
em vez de substituído. Na prática de papel, o documento viciado é frequentemente
retirado e substituído, e o rasto perde-se. O formato não julga o ato; preserva o
que permite julgá-lo, e regista o julgamento como facto documental.

**O teste corta para os dois lados.** Aquilo que um verificador decide com o
pacote em mãos é exatamente aquilo que o formato pode impor — e, portanto,
melhorar:

| Contributo real para a qualidade | Onde vive |
|---|---|
| Completude estrutural do tipo — campos obrigatórios, `additionalProperties: false` | schema de `tipo_documento_ref` |
| Recusa de finalização com avaliação irresolúvel ou nível de assinatura sem certificado conforme | pré-condições de finalização (SPEC §5.1) |
| Menção de imputação jurídica, frequentemente ausente ou implícita em prática de papel | `imputacao` (SPEC §2.15) |
| Proveniência de sistema e de IA declaradas | SPEC §2.13, §2.14 |

Isto é normalidade estrutural, não legalidade substantiva — mas é normalidade
que o percurso `Word → impressão → assinatura` não tem forma de garantir nem de
medir.

## Consequências

**Positivas**: o projeto passa a ter critério de **inclusão**, que faltava, a
par do critério de exclusão do teste de admissão. Os dois limitam o formato
pelos dois lados; sem o segundo, o primeiro só sabe dizer que não.

Aplicado retrospetivamente, o critério confirma três decisões e reclassifica
uma: os `componentes[].sha256` têm de poder viver nos bytes assinados
(ADR-021); a ausência de estratégia de reconstituição tem de ser expressável; e
a cadeia de custódia, hoje, **não pode** acompanhar uma transferência entre
entidades — sendo relevante e necessária, isso é lacuna do formato e não da
operação.

**Negativas / mitigações**: um `.ndfpkg` válido garante menos do que muitos
leitores assumirão — garante integridade, identidade e interpretabilidade, não
legalidade, completude nem correção. O risco manifesta-se em três sítios: o
`validation_code` que confere e dá impressão de aval oficial; o rótulo igual
para as duas realidades de ADR-020; e o formulário que valida a verde e ensina
o operador que fez bem, quando só se verificou a forma.

São três instâncias do mesmo problema e pedem uma resposta única: **uma doutrina
de projeto sobre o que o NORMORDIS diz quando algo passa** — nunca «válido» sem
dizer o que foi verificado. Não é matéria de formato; é matéria do projeto, e
está registada como trabalho próprio.

**Sobre alegações de qualidade**: «melhora a qualidade dos atos» é empírico e
cai sob os gates de [`READINESS.md`](../normalization/READINESS.md); sem corpus
comparativo (`R6`) é alegação, não evidência. A versão defensável é mais
estreita e mais forte — **completude estrutural mensurável, onde antes não havia
nada a medir**.

## Referências

- SPEC.md §1.1, §1.4, §2.13.1 (limites de garantia), §5.1 (pré-condições), §5.3 (imutabilidade), §2.11.2 (`anula`)
- [`LACUNAS.md`](../../LACUNAS.md) — L1, princípio de âmbito
- [`ROADMAP.md`](../../ROADMAP.md) — teste de admissão (2026-08-15)
- [`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md) §7.4
- ADR-015 (não abstrair por antecipação), ADR-020, ADR-021
