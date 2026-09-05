# Reporting regulatório — Cyber Resilience Act (CRA)

## Estado e âmbito desta política

Este documento assume, por precaução, que o ecossistema NORMORDIS (incluindo
`normordis-formats` e `normordis-pdf`) pode vir a ser considerado "produto com
elementos digitais" nos termos do Regulamento (UE) 2024/2847 (Cyber
Resilience Act), dado o seu propósito declarado — sistemas institucionais,
não um projeto pessoal incidental. **Isto não é uma determinação jurídica
formal**; é uma decisão prática de estar preparado antes de confirmar a
classificação exata com aconselhamento jurídico, à medida que o projeto for
adotado por terceiros.

Este documento cobre a **obrigação de reporting regulatório** (Artigo 14 do
CRA) — a notificação de vulnerabilidades ativamente exploradas ou incidentes
graves à autoridade competente. É diferente e complementar ao
[`SECURITY.md`](SECURITY.md), que cobre o canal de **entrada**: como alguém
de fora comunica uma vulnerabilidade ao mantenedor.

```text
SECURITY.md         → entrada: alguém reporta-nos uma vulnerabilidade
CRA_REPORTING.md     → saída: nós reportamos à autoridade, se aplicável
```

## Quando se aplica (gatilho)

Só desencadeia a obrigação de reporting regulatório se, para uma versão
publicada de `normordis-formats` ou `normordis-pdf`:

- houver uma vulnerabilidade **ativamente explorada** (evidência real de
  exploração, não apenas existência teórica); ou
- ocorrer um **incidente grave de segurança** com impacto na segurança do
  produto (não necessariamente uma vulnerabilidade de código — pode ser,
  por exemplo, comprometimento da cadeia de distribuição/build).

Uma vulnerabilidade comunicada normalmente via `SECURITY.md`, sem indícios de
exploração ativa, **não** desencadeia este procedimento — segue o fluxo
normal de correção e advisory GitHub.

## Prazos (Artigo 14 CRA)

Os primeiros dois prazos contam a partir do momento em que o mantenedor toma
conhecimento do evento. O relatório final tem uma âncora diferente consoante
o caso — não é a deteção inicial:

| Fase | Prazo | Contado a partir de | Conteúdo |
|---|---|---|---|
| Aviso prévio (early warning) | ≤ 24 horas | Conhecimento do evento | Existência do evento, indicação preliminar de causa/âmbito |
| Notificação | ≤ 72 horas | Conhecimento do evento | Detalhes técnicos, avaliação de gravidade e impacto, medidas de mitigação disponíveis |
| Aviso a utilizadores afetados — ver secção própria abaixo | Sem demora indevida | Assim que a informação e as medidas de mitigação estiverem disponíveis | Aviso do evento e medidas que os utilizadores podem aplicar |
| Relatório final — vulnerabilidade ativamente explorada | ≤ 14 dias | Disponibilização de uma medida corretiva ou de mitigação | Descrição completa, causa raiz, medidas corretivas aplicadas |
| Relatório final — incidente grave sem vulnerabilidade associada | ≤ 1 mês | Notificação de 72h (não a deteção inicial) | Descrição completa, causa raiz, medidas aplicadas |

Enquanto a correção de uma vulnerabilidade não existir, os 14 dias do
relatório final **ainda não começaram a contar** — não há prazo-limite a
"falhar" nesse intervalo. Nesse período, mantém-se a Single Reporting
Platform informada do progresso conforme razoável; assim que a medida
corretiva ou de mitigação for disponibilizada, os 14 dias começam a contar
a partir dessa data.

## Canais de notificação

A notificação ao abrigo do Artigo 14 é submetida **uma única vez**, através
da:

1. **ENISA — Single Reporting Platform (SRP)**, plataforma única europeia
   exigida pelo Artigo 14(3), operacional a partir de 11 de setembro de 2026.
   A submissão na SRP é distribuída automaticamente à ENISA e ao CSIRT
   coordenador selecionado — não se submete o mesmo evento em separado a
   outro canal.
   - Página oficial: <https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp>
   - Acesso via EU Login — **a conta pode e deve ser criada antecipadamente**,
     mesmo antes de existir um evento a reportar, para não perder tempo no
     momento de uma notificação real.
   - O URL de acesso direto à plataforma só é publicado pela ENISA pouco
     antes do go-live — confirmar na página oficial acima antes de cada uso,
     não assumir que este documento tem o link definitivo.
   - Ao criar a conta, confirmar como CSIRT coordenador o **CERT.PT**,
     serviço do CNCS (Centro Nacional de Cibersegurança) e autoridade
     competente NIS2/CRA em Portugal.

2. **CERT.PT — canal direto, apenas como reserva** (SRP indisponível, fora
   de serviço, ou antes do go-live de 11/09/2026). Não usar em paralelo com
   a SRP para o mesmo evento quando ambas estão operacionais — criaria
   tratamento duplicado do mesmo relatório.
   - Notificação de incidente: <https://www.cncs.gov.pt/pt/notificacao-incidentes/>
   - Email: `cert@cert.pt`
   - Telefone: +351 210 497 399 (permanência 24/7: +351 910 599 284)

> Ação pendente para o mantenedor: criar a conta EU Login e confirmar o CSIRT
> coordenador (CERT.PT) no registo assim que a SRP estiver acessível. Registar
> aqui a data em que isto for feito.

## Fluxo interno (mantenedor único)

```text
1. Deteção/conhecimento do evento
   (via SECURITY.md, scanning de dependências, alerta externo, etc.)
        ↓
2. Triagem imediata: é exploração ativa ou incidente grave?
   ├─ Não → segue fluxo normal de SECURITY.md (sem obrigação CRA)
   └─ Sim ↓
3. Early warning ≤ 24h → ENISA SRP (distribui a CERT.PT como coordenador)
        ↓
4. Notificação ≤ 72h → detalhes técnicos e mitigação, via SRP
        ↓
5. Aviso aos utilizadores afetados, sem demora indevida, assim que houver
   informação e mitigação a comunicar (ver secção própria) — não esperar
   pela correção definitiva para isto
        ↓
6. Corrigir, publicar patch release, advisory GitHub
        ↓
7. Relatório final: ≤ 14 dias após a correção/mitigação existir
   (vulnerabilidade), ou ≤ 1 mês após a notificação de 72h
   (incidente sem vulnerabilidade associada)
        ↓
8. Registar entrada em docs/compliance/CRA-REPORTS-LOG.md
```

Dado que o mantenedor é único, não há separação entre quem deteta, decide e
reporta — a triagem do passo 2 deve ser feita com cautela adicional
precisamente por não haver um segundo par de olhos; em caso de dúvida sobre
se um evento qualifica, o mais prudente é reportar (o custo de um aviso
prévio desnecessário é baixo; o de silêncio sobre um evento que qualificava
não é).

## Aviso a utilizadores afetados (Artigo 14(4))

A notificação à autoridade (SRP/CERT.PT) **não substitui** o dever de avisar
os utilizadores. O Artigo 14(4) exige, sem demora indevida e após a
notificação à autoridade, informar:

- os **utilizadores afetados** pela vulnerabilidade ativamente explorada ou
  pelo incidente grave; e, quando apropriado,
- **todos os utilizadores**, se o alcance do evento o justificar.

O aviso deve incluir, no mínimo:

- natureza do evento e produto(s)/versão(ões) NORMORDIS afetados;
- qualquer medida de mitigação que o utilizador possa aplicar de imediato
  (ex.: desativar uma funcionalidade, restringir acesso, atualizar uma
  dependência), mesmo antes de existir uma correção definitiva;
- quando disponível, a correção e como aplicá-la.

Canais para este aviso: advisory de segurança do GitHub no repositório
afetado (`normordis-formats` e/ou `normordis-pdf`), entrada no `CHANGELOG.md`
e, se existirem, os canais de distribuição adicionais do projeto. Este aviso
é distinto do "advisory GitHub" final mencionado no fluxo — pode e deve sair
mais cedo, com a informação disponível nesse momento, e ser atualizado depois.

## Registo de evidência

Cada notificação feita (ou decisão fundamentada de não notificar um evento
limite) fica registada em
[`docs/compliance/CRA-REPORTS-LOG.md`](docs/compliance/CRA-REPORTS-LOG.md).
Nunca incluir segredos, credenciais ou dados pessoais reais nesse registo —
apenas datas, identificadores públicos (CVE, advisory GitHub) e resumo do
evento.

## Aplicação a `normordis-pdf`

Este documento é a referência única para todo o ecossistema NORMORDIS. O
`normordis-pdf` remete para aqui a partir do seu próprio `SECURITY.md`, em
vez de duplicar o procedimento.
