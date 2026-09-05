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

A partir do momento em que o mantenedor toma conhecimento do evento:

| Fase | Prazo | Conteúdo |
|---|---|---|
| Aviso prévio (early warning) | ≤ 24 horas | Existência do evento, indicação preliminar de causa/âmbito |
| Notificação | ≤ 72 horas | Detalhes técnicos, avaliação de gravidade e impacto, medidas de mitigação disponíveis |
| Relatório final | ≤ 14 dias (vulnerabilidade) ou ≤ 1 mês (incidente sem vulnerabilidade associada) | Descrição completa, causa raiz, medidas corretivas aplicadas |

Se a correção ainda não estiver disponível ao fim de 14 dias, é submetido um
relatório intercalar, seguido do relatório final quando a correção existir.

## Canais de notificação

Reporta-se **uma vez**, em simultâneo, via:

1. **CSIRT nacional** — Portugal: **CERT.PT**, serviço do CNCS (Centro
   Nacional de Cibersegurança), autoridade competente NIS2 e ponto de
   contacto único nacional.
   - Notificação de incidente: <https://www.cncs.gov.pt/pt/notificacao-incidentes/>
   - Email: `cert@cert.pt`
   - Telefone: +351 210 497 399 (permanência 24/7: +351 910 599 284)
2. **ENISA — Single Reporting Platform (SRP)**, plataforma única europeia,
   operacional a partir de 11 de setembro de 2026.
   - Página oficial: <https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp>
   - Acesso via EU Login — **a conta pode e deve ser criada antecipadamente**,
     mesmo antes de existir um evento a reportar, para não perder tempo no
     momento de uma notificação real.
   - O URL de acesso direto à plataforma só é publicado pela ENISA pouco
     antes do go-live — confirmar na página oficial acima antes de cada uso,
     não assumir que este documento tem o link definitivo.

> Ação pendente para o mantenedor: criar a conta EU Login e confirmar o CSIRT
> designado (CERT.PT) no registo assim que a SRP estiver acessível. Registar
> aqui a data em que isto for feito.

## Fluxo interno (mantenedor único)

```text
1. Deteção/conhecimento do evento
   (via SECURITY.md, scanning de dependências, alerta externo, etc.)
        ↓
2. Triagem imediata: é exploração ativa ou incidente grave?
   ├─ Não → segue fluxo normal de SECURITY.md (sem obrigação CRA)
   └─ Sim ↓
3. Early warning ≤ 24h → CERT.PT + ENISA SRP
        ↓
4. Notificação ≤ 72h → detalhes técnicos e mitigação
        ↓
5. Corrigir, publicar patch release, advisory GitHub
        ↓
6. Relatório final ≤ 14 dias / 1 mês
        ↓
7. Registar entrada em docs/compliance/CRA-REPORTS-LOG.md
```

Dado que o mantenedor é único, não há separação entre quem deteta, decide e
reporta — a triagem do passo 2 deve ser feita com cautela adicional
precisamente por não haver um segundo par de olhos; em caso de dúvida sobre
se um evento qualifica, o mais prudente é reportar (o custo de um aviso
prévio desnecessário é baixo; o de silêncio sobre um evento que qualificava
não é).

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
