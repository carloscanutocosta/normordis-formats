# ADR-020: Um formato para documento nativo e documento capturado

**Estado**: Aceite
**Data**: 2026-08-20
**Decisores**: carloscanutocosta

---

## Contexto

O editor estruturado NORMORDIS cobrirá progressivamente as tipologias
administrativas correntes, mas não as cobre hoje e não cobrirá tão cedo a
totalidade. O fluxo real dos serviços é `Word → PDF → impressão → assinatura`,
e existe uma segunda categoria, independente da primeira: documentos que
**chegam de fora** — requerimento digitalizado, submissão via e-balcão,
certidão de outra entidade, ficheiro anexo a correio eletrónico — e cuja guarda
é juridicamente necessária.

Nenhuma das duas categorias tem hoje representação NDF. SPEC §2.8 exclui-as
expressamente, ao declarar que a especificação «cobre apenas documentos gerados
internamente sem anexos binários opacos».

A questão de desenho é se estas categorias exigem um formato próprio — um
contentor de preservação separado, ao lado do NDF — ou se cabem no NDF.

## Decisão

**Um só formato.** O NDF cobre as duas realidades. Um documento não nascido no
editor estruturado é um NDF cujo `metadados.tipo_documento_ref` é
`documento-capturado@<versao>` e cujo `documento` declara os componentes
binários por hash.

Isto **não** é alargamento do NDF-core. SPEC §2.9.1 já declara que o NDF-core é
um envelope genérico e que `documento` é intencionalmente opaco a esse nível,
tipado por schema próprio, para acomodar «qualquer tipologia futura […] sem
necessidade de revisão major desta especificação». `documento-capturado` é uso
desse mecanismo, não excepção a ele.

**Um tipo genérico, não uma família.** Não se criam `oficio-capturado`,
`parecer-capturado` e semelhantes. Um campo opcional `tipo_equivalente`
regista, quando determinável, qual o tipo nativo que o documento teria se
tivesse sido produzido no editor estruturado.

## Alternativas consideradas

### Formato de preservação separado, ao lado do NDF

**Prós**: a diferença de garantias ficaria óbvia pelo nome; nenhum risco de
alegar para um capturado o que só o nativo oferece.

**Contras**: duplicaria tudo o que não difere. O grafo documental partir-se-ia
em dois — um despacho nativo não poderia decidir sobre um requerimento
capturado sem um mecanismo de ponte, e as pontes apodrecem. O regime
arquivístico duplicar-se-ia: `avaliacao`, PCA/DF e perfis teriam duas
implementações para a mesma decisão jurídica. A cadeia de custódia, indexada
por `ndf_id`, deixaria de servir os dois. A conformidade exigiria duas suites, e
a segunda ficaria permanentemente atrás da primeira. E deixaria uma costura
permanente no arquivo, precisamente no momento em que o editor estruturado
passasse a cobrir uma tipologia que antes era capturada.

### Alargar o NDF-core com primitivas de captura

Falha o passo 2 do teste de admissão de novas primitivas
([`ROADMAP.md`](../../ROADMAP.md), 2026-08-15): o que cabe em `documento` via
schema do tipo tem aí o seu lugar, não no core.

### Mapear semanticamente o formato de origem para o NDF nativo

Exigiria um parser por formato de origem, válido apenas para templates
conhecidos à partida, e um subconjunto suportado definido e mantido. Não
generaliza, e conflaciona a camada de dados com a camada de documento — o mesmo
erro já identificado e recusado em `R13`.

## Justificação da decisão

A diferença entre as duas realidades está **confinada a um bloco**. São
rigorosamente iguais: `ndf_id`, `estado`, `nivel_assinatura`,
`payload_hash_alg`, `metadados`, `avaliacao`, `relacoes`, `participantes`,
`imputacao`, `proveniencia_sistema`, `proveniencia_ia`, o envelope CAdES-B-LTA
com timestamps e material de validação, o `validation_code` e a cadeia de
custódia. Nos dois casos existem `payload_bytes`, existe `payload_hash`, e a
assinatura cobre exatamente a mesma coisa.

Diferem em duas coisas, e só nessas:

1. **`documento`** — no nativo contém o ato; no capturado contém a casca
   descritiva e os componentes. O corpo do ato desce para dentro do binário.
2. **A função de `ndt_version_ref`** — no nativo o NDT é gerativo, é a instrução
   a partir da qual o documento se produz visualmente; no capturado é
   descritivo, renderiza o auto de captura e não o documento.

Em termos das camadas de
[`CRITERIO-DE-CAMADAS.md`](../design/CRITERIO-DE-CAMADAS.md) §4: **a captura
colapsa as camadas 2, 3 e 4 num único artefacto opaco, e mantém intactas a 1 e
a 5.**

Um NDF capturado não é, portanto, um NDF degradado. É um NDF completo cujo
`documento` aponta para fora.

## Consequências

**Positivas**: um só grafo documental, um só regime arquivístico, uma só cadeia
de custódia, um só verificador, uma só afirmação jurídica. E corpus homogéneo
através da transição — quando o editor passar a cobrir uma tipologia, os
documentos nativos são o mesmo tipo de objeto que os capturados que os
precederam.

**Negativas / mitigações**: o rótulo igual pode sugerir garantias iguais. É o
único argumento sério a favor da separação, e a mitigação é dupla e obrigatória:

- **normativa** — um leitor conforme NÃO DEVE renderizar um documento capturado
  aplicando o seu NDT a `documento` como se fosse conteúdo; tem de resolver o
  componente. Sem este requisito, «um formato» degenera em «um formato com dois
  comportamentos silenciosos»;
- **de comunicação** — a paridade entre as duas vias é de custódia, integridade
  e proveniência, **não** de reconstituição nem de agilidade de apresentação. O
  documento capturado falha por construção o teste de longevidade de
  `CRITERIO-DE-CAMADAS.md` §7: está congelado numa projeção e não se reprojeta
  para um formato futuro.

A distinção é verificável por inspeção, sem heurística:
`metadados.tipo_documento_ref` igual a `documento-capturado@<versao>`.

## Referências

- SPEC.md §2.8 (tipos de conteúdo permitidos), §2.9.1 (envelope genérico), §9.2 (leitor conforme)
- [`ROADMAP.md`](../../ROADMAP.md) — teste de admissão (2026-08-15); decisão de âmbito sobre §2.8 (2026-08-20)
- [`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md) §3
- [`docs/design/CRITERIO-DE-CAMADAS.md`](../design/CRITERIO-DE-CAMADAS.md) §4, §7
- ADR-021 (componentes nos bytes assinados), ADR-022 (dever do formato)
