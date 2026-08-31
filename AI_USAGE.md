# Política de Utilização de IA Generativa

**Estado:** política em vigor, aplicável a todo o ecossistema NORMORDIS.
**Em vigor desde:** 2026-08-31 <!-- CONFIRMAR: ver §10 -->
**Responsável pelo projeto:** Carlos Canuto Costa
**Última revisão:** 2026-08-31

## 1. Postura geral

Este projeto utiliza ferramentas de IA generativa — atualmente **Claude Code**
(modelos Claude da Anthropic) — como auxiliar de implementação sob controlo
arquitetural humano. A IA não substitui responsabilidade humana em nenhuma fase
de decisão.

Formulação operacional:

> *AI-assisted development under human architectural control, with documented
> provenance, mandatory review, conformance testing independent from the
> generating session, and human accountability for every deliverable.*

Esta política existe para dar resposta verificável às obrigações de
transparência da política GenAI da NLnet, e é publicada independentemente de
qualquer decisão de financiamento.

## 2. Âmbito

| Repositório | Natureza | Licença | Uso de IA previsto |
|---|---|---|---|
| `normordis-formats` | Especificações, schemas, vetores de conformidade | CC0-1.0 | Marginal — ver §4 |
| `normordis-kernel` | Implementação | EUPL-1.2 | Geração de código sob revisão |
| `normordis-go` | Implementação | EUPL-1.2 | Geração de código sob revisão |
| `normordis-pdf` | Implementação | *(por fixar)* | Geração de código sob revisão |
| `normordis-cloud-sync` | Implementação | EUPL-1.2 | Restrições adicionais — ver §7 |
| `core-ui` | Implementação | EUPL-1.2 | Geração de código sob revisão |

Este ficheiro é a versão canónica. Os repositórios de implementação remetem
para aqui em vez de manterem cópias divergentes.

## 3. O que permanece exclusivamente humano

As decisões seguintes são tomadas, redigidas e assumidas por pessoa
identificada, sem delegação a sistemas generativos:

- especificação e design dos formatos (NDF, NDT, NCRTF, `.ndfpkg`) e respetivos
  schemas;
- decisões de arquitetura — separação de responsabilidades, escolha de
  dependências, modelo de segurança, modelo criptográfico;
- requisitos de conformidade com normas externas (PDF/A, PDF/UA-2,
  CAdES-B-LTA, ISO, ETSI, RFC aplicáveis);
- critérios de aceitação e avaliação de cada entregável;
- revisão e aprovação final de qualquer alteração antes de integração.

## 4. O que pode ser assistido por IA

Sempre com revisão humana registada:

- geração de código de implementação a partir de especificação já fixada;
- sugestões de refactoring;
- geração de testes, nunca como única fonte de verdade de conformidade (§5);
- documentação, tradução e revisão editorial.

Neste repositório em concreto, o texto normativo das especificações é de
autoria humana. A assistência de IA, quando usada, limita-se a revisão
editorial, verificação de consistência entre texto, schema e vetores, e
deteção de contradições — não à formulação de requisitos normativos.

## 5. Testes de conformidade independentes da sessão geradora

A garantia mais forte do projeto não é declarativa, é estrutural.

A governação NORMORDIS já separa especificação de implementação: as
especificações são normativas e residem neste repositório; as implementações
de referência não têm autoridade normativa (ver [GOVERNANCE.md](GOVERNANCE.md)
e [CONFORMANCE.md](CONFORMANCE.md)). Os vetores de conformidade em
`conformance/` derivam do texto normativo, não do código que os deve passar.

Consequência prática: uma implementação assistida por IA é avaliada contra
uma suite que não foi produzida pela sessão que a gerou, nem a partir dela.
Uma suite de testes gerada pela mesma sessão que produziu a implementação não
constitui evidência de conformidade e não é aceite como tal.

Adicionalmente, os casos negativos exigem rejeição **pela violação que
documentam** (`_expected_match`), o que impede que uma implementação passe a
suite por defeito acidental.

## 6. Originalidade e licenciamento

Antes de integrar qualquer output assistido:

- verifica-se que o output não reproduz material protegido incompatível com a
  licença do repositório de destino (CC0-1.0 para especificações, EUPL-1.2 para
  implementações);
- consultam-se os termos de utilização da ferramenta quanto à titularidade e
  originalidade dos outputs;
- nenhum output puramente gerado, sem contribuição intelectual humana
  substancial, é apresentado como entregável elegível para pagamento.

**Nota específica sobre CC0-1.0.** A CC0 é uma renúncia de direitos, o que
pressupõe que quem a aplica é titular dos direitos a renunciar. Material cuja
titularidade seja duvidosa não é adequado a dedicação CC0. Por essa razão, o
texto normativo e os vetores de conformidade deste repositório são de autoria
humana (§4), e não se aplica CC0 a blocos substanciais de texto gerado.

**Pendente:** `normordis-pdf` não tem ficheiro de licença. Deve ser fixado
antes de qualquer submissão que o inclua como entregável.

## 7. Regras de revisão e aceitação de código assistido

Nenhum output é integrado sem que o responsável humano possa, sem consultar a
ferramenta:

1. explicar o que o código faz e por que razão está escrito assim;
2. identificar a decisão arquitetural ou o requisito normativo que o justifica;
3. indicar o que aconteceria se falhasse.

Critérios de rejeição — o output é descartado ou reescrito quando:

- introduz dependência não aprovada previamente;
- altera comportamento observável coberto por especificação sem alteração
  normativa correspondente;
- não é acompanhado de teste derivado da especificação;
- contém lógica criptográfica, de assinatura ou de cadeia de custódia que o
  revisor não consiga verificar linha a linha contra a norma aplicável.

**Restrição reforçada — `normordis-cloud-sync`.** Código de autenticação,
gestão de credenciais, OAuth, armazenamento de segredos e controlo de acesso
não é aceite a partir de geração assistida sem revisão linha a linha e teste
específico. Não se aplica aqui a prática de aceitar boilerplate por analogia.

**Restrição absoluta.** Nenhum segredo, credencial, chave privada ou conteúdo
de `secrets/` é fornecido a ferramentas de IA, em nenhuma circunstância.

## 8. Registo de proveniência

A convenção de registo em histórico git está em
[docs/ai-provenance.md](docs/ai-provenance.md).

O log de proveniência de prompts exigido na **fase de candidatura** é distinto
e não se confunde com este: ver
[docs/genai-application-disclosure-template.md](docs/genai-application-disclosure-template.md).

## 9. Resposta a pedidos de esclarecimento

Este documento foi estruturado para servir de resposta direta caso seja pedido
detalhe sobre a extensão do uso de IA generativa no projeto:

| Pergunta previsível | Onde está a resposta |
|---|---|
| Que ferramentas e modelos são usados? | §1 |
| Em que partes do projeto? | §2, §4 |
| O que não é delegado a IA? | §3 |
| Como se evita auto-validação da suite de testes? | §5 |
| Como se trata originalidade e licenciamento? | §6 |
| Que revisão humana existe antes da integração? | §7 |
| Como se verifica a proveniência a posteriori? | §8 |
| Desde quando se aplica? | §10 |

Comprometemo-nos a fornecer, a pedido, detalhe adicional sobre entregáveis
concretos, incluindo prompts e outputs não editados que estejam registados.

## 10. Âmbito temporal

Esta política aplica-se a partir da data indicada no cabeçalho, a todo o
trabalho iniciado após essa data. Não é aplicada retroativamente ao histórico
anterior, e não se reconstrói proveniência para trabalho já realizado — uma
reconstrução a posteriori seria, ela própria, menos fiável do que a sua
ausência declarada.

O projeto não beneficia de qualquer exceção para projetos em curso: não existe
acordo de financiamento anterior. A disclosure aplica-se integralmente desde a
data acima.

## 11. Contacto

Questões sobre o uso de IA neste projeto: carloscanutocosta@gmail.com

---

*As referências à política GenAI da NLnet devem ser confirmadas contra o texto
em vigor à data de submissão. Esta política é substantiva por si própria e não
depende dessa confirmação.*
