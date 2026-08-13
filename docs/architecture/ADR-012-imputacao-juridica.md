# ADR-012: Imputação jurídica como eixo único do NDF-core

**Estado**: Aceite
**Data**: 2026-08-13
**Decisores**: carloscanutocosta

---

## Contexto

O NDF sabe registar **quem assina** (envelope, §4), **quem interveio
materialmente** (`participantes`, §2.12) e **que IA interveio**
(`proveniencia_ia`, §2.13). Não sabe registar **quem responde juridicamente
pelo documento, e a que título**.

Isto não é uma lacuna estética. É uma exigência legal expressa, em dois
regimes distintos.

**Regime do ato administrativo.** O CPA (art. 151.º, n.º 1, alínea a))
determina que do ato deve constar "a indicação da autoridade que o pratica e
a menção da delegação ou subdelegação de poderes, quando exista". O CPPT
(art. 36.º, n.º 2) repete a exigência para as notificações, que devem conter
"a indicação da entidade que o praticou e se o fez no uso de delegação ou
subdelegação". E o CPPT (art. 66.º, n.º 2) dirige o recurso hierárquico "ao
mais elevado superior hierárquico do autor do ato" — sem identificação do
órgão autor não se determina o destinatário do recurso nem se controla a
competência.

**Regime declarativo.** O Código do IRS produz quatro casos distintos sobre
o mesmo documento (Modelo 3):

| Caso | Conteúdo produzido por | Responde juridicamente |
|---|---|---|
| Art. 56.º — declaração do sujeito passivo | o próprio | o próprio |
| Art. 58.º-A — automática, confirmada | sistema da AT | sujeito passivo, por confirmação |
| Art. 58.º-A — automática, convertida sem confirmação | sistema da AT | sujeito passivo, **por efeito legal** |
| Art. 76.º, n.º 1, al. b) — liquidação oficiosa | sistema da AT | órgão da AT |

O terceiro caso é o que expõe o problema com nitidez. Não havendo confirmação
nem entrega até ao termo do prazo, a declaração provisória converte-se em
declaração apresentada pelo sujeito passivo nos termos legais. A autoria é
imputada por ficção legal a quem não produziu o conteúdo nem praticou
qualquer ato. Nesse caso:

- `participantes[].papel = "autor"` com o sujeito passivo seria juridicamente
  correto e **factualmente falso** — ele não redigiu nada;
- `proveniencia_sistema` sozinho seria factualmente correto e
  **juridicamente incompleto** — perder-se-ia que a declaração é dele para
  todos os efeitos, incluindo responsabilidade contraordenacional.

`metadados.entidade_produtora` (§2.7.3) não resolve nenhum destes casos: é a
pessoa coletiva para efeitos arquivísticos (designação, NIF, código DGLAB),
não o órgão nem a pessoa que responde.

## Decisão

Introduzir um campo de topo opcional `imputacao`, **array**, como eixo único
de responsabilidade jurídica:

```json
"imputacao": [
  {
    "imputado": { "designacao": "Diretor de Serviços do IRS", "ref": "at:dsirs" },
    "titulo": "delegacao",
    "fundamento": {
      "descricao": "Despacho n.º 000/2026",
      "publicacao_ref": "DR, 2.ª série, n.º 000, de 2026-01-15"
    }
  }
]
```

`titulo` cobre os dois regimes num só vocabulário:

- **ato administrativo**: `competencia_propria`, `delegacao`, `subdelegacao`;
- **declarativo**: `declaracao_propria`, `aceitacao_expressa`, `efeito_legal`.

Com condicionais: `delegacao` e `subdelegacao` exigem
`fundamento.publicacao_ref` (é a menção que o CPA manda fazer);
`aceitacao_expressa` exige `em`; `efeito_legal` exige `fundamento.descricao`.

Mais do que uma entrada significa **co-titularidade da responsabilidade** —
ato conjunto de dois ou mais órgãos, ou declaração conjunta de dois ou mais
declarantes. Nunca cadeia de delegação: a delegação é uma entrada só, com o
título e o fundamento a identificar o delegante.

Cada entrada admite ainda um bloco opcional `autenticacao`
(`{ meio, nivel_garantia }`), que regista o facto em que a imputação assenta
quando o documento é submetido por canal autenticado — Portal das Finanças,
Segurança Social Direta, e-balcão — ou apresentado presencialmente por
interessado identificado. Três decisões associadas:

1. **Por entrada, não por documento.** Onde a lei exige autenticação de mais
   do que um interessado — a declaração de IRS em tributação conjunta exige a
   de ambos os sujeitos passivos —, cada um tem entrada, instante e meio
   próprios. Registar ao nível do documento perderia exatamente a informação
   que demonstra o cumprimento da exigência legal.
2. **A imputação não é qualificável.** Não existe mecanismo para exprimir grau
   de confiança, presunção ou reserva. Um documento submetido por meio
   autenticado é imputado ao titular das credenciais, sem gradação; alegações
   de uso indevido dirimem-se judicialmente, fora do formato.
3. **`meio` inclui o presencial.** Um pedido por e-balcão e um pedido ao
   balcão por interessado identificado têm o mesmo valor jurídico; um
   vocabulário só de meios digitais obrigaria a modelar o caso presencial por
   omissão, tornando-o indistinguível de um documento sem identificação.

O registo de autenticação é **prova, não autorização**: fundamenta tanto a
imputação de autoria como a legitimidade de acesso a informação sob sigilo,
mas o NDF não define nem verifica controlo de acesso (§1.5).

## Alternativas consideradas

### Dois blocos separados — `autoridade_ato` e `imputacao_conteudo`

Foi a formulação inicial, e é a intuitiva: um bloco para o órgão que pratica
o ato administrativo, outro para a imputação de conteúdo declarativo.

**Prós**: cada bloco tem vocabulário homogéneo, de um só regime jurídico;
as condicionais de validação não se misturam.

**Contras**: os dois respondem exatamente à mesma pergunta — quem responde
juridicamente, e a que título — variando apenas o regime do título. Separá-los
garante que o primeiro caso que não seja nem ato administrativo nem declaração
fiscal (autorizações tácitas do CPA, atos de execução, deferimento por
silêncio, atos de outros organismos) exigiria um terceiro bloco de topo. A
fusão transforma esses casos em valores novos de `titulo`, que é uma alteração
aditiva, em vez de blocos novos, que são alterações estruturais. Rejeitado por
produzir acumulação onde a generalização é possível.

### Papel novo em `participantes`

**Prós**: nenhum campo de topo novo; reutiliza estrutura existente.

**Contras**: três razões independentes. `participantes` é um índice de pessoas
singulares com referências opacas e não resolvidas (§2.12.4), ao passo que a
menção de delegação é conteúdo normativo do próprio ato, com publicação em
Diário da República — natureza diferente. Um órgão não é uma pessoa singular.
E no caso da conversão do art. 58.º-A não há ato de pessoa nenhuma a registar:
o facto jurídico é o decurso do prazo, que um índice de participantes não
consegue representar. Rejeitado.

### Deixar ao schema de cada tipo documental

**Prós**: máxima flexibilidade por tipo; nenhuma alteração ao NDF-core.

**Contras**: a informação seria repetida em cada tipo documental, com
estruturas divergentes entre entidades, e um leitor genérico deixaria de
conseguir responder "quem responde por este documento" sem conhecer o schema
do tipo. É precisamente o género de dado transversal que justifica existir
NDF-core. Rejeitado.

## Justificação da decisão

A decisão dá ao NDF uma dualidade limpa entre facto e direito:

| Eixo | Pergunta | Natureza |
|---|---|---|
| `participantes[]` | que pessoa produziu materialmente | facto |
| `proveniencia_sistema[]` / `proveniencia_ia` | que máquina produziu | facto |
| `imputacao[]` | quem responde, e a que título | direito |

Os eixos factuais registam o que o sistema produtor observou. O eixo jurídico
regista o que a lei imputa. São independentes por desenho: podem coincidir
(art. 56.º), divergir (art. 58.º-A confirmada) ou ser mutuamente exclusivos
(art. 58.º-A convertida, onde não há autor humano e a imputação é a uma
pessoa que nada fez).

`imputacao` é opcional no NDF-core porque nem todo o NDF é ato administrativo
ou declaração — uma informação técnica interna não tem imputação no sentido
aqui definido. O schema do tipo documental pode torná-la obrigatória, camada
de exigência já usada noutros pontos da especificação.

## Consequências

**Positivas**: o NDF passa a suportar as menções obrigatórias do CPA art.
151.º/1/a) e do CPPT art. 36.º/2, e a identificar o autor do ato para efeitos
do CPPT art. 66.º/2; documentos gerados automaticamente deixam de ficar sem
responsável identificável; regimes futuros entram como valores de `titulo`.

**Negativas / mitigações**: um só bloco acumula condicionais de dois regimes
jurídicos, o que torna o JSON Schema mais denso (if/then por `titulo`) —
aceite como o custo da generalização, e contido por as condicionais serem
independentes entre si. Risco de confusão com `metadados.entidade_produtora`
— mitigado por nota explícita em §2.7.3 e §2.15.

**Compatibilidade**: aditivo. Nenhum documento produzido antes desta alteração
deixa de validar por causa deste campo.

## Referências

- SPEC.md §2.15, §2.7.3, §9.1, §9.2
- CPA, art. 151.º, n.º 1, al. a); CPPT, art. 36.º, n.º 2 e art. 66.º, n.º 2
- CIRS, art. 56.º, art. 58.º-A e art. 76.º, n.º 1, al. b)
- ADR-006-participantes-vs-signatarios.md
- ADR-013-proveniencia-sistema.md
