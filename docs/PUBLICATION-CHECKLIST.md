# Checklist de publicação pública

Esta lista serve para abrir o repositório ao público sem abrir a gestão a
alterações não revistas. Execute-a antes de alterar a visibilidade no GitHub.

## Conteúdo e histórico

- [ ] Confirmar que `main`, `devel` e `lab` são todos adequados a publicação;
  quando um repositório passa a público, todas as branches e respetivo histórico
  alcançável ficam públicos.
- [ ] Rever os endereços de e-mail do histórico Git; também passam a ser
  públicos. Prefira um endereço `noreply` do GitHub para commits futuros, se
  necessário.
- [ ] Executar uma deteção de segredos no histórico completo (por exemplo,
  `gitleaks git --redact`) e rodar credenciais caso seja encontrado algo.
- [ ] Confirmar que exemplos, PDFs, fixtures e anexos só contêm dados sintéticos
  ou que podem ser publicados legalmente.
- [ ] Confirmar que os ficheiros locais agora ignorados não estavam já
  versionados: `git ls-files .env '*.pem' '*.key' '*.p12' '*.pfx'`.

## Configurações do GitHub

- [ ] Em **Settings → General**, alterar a visibilidade para **Public** apenas
  depois da revisão anterior.
- [ ] Em **Settings → Branches**, proteger `main`: exigir pull request, uma
  aprovação, *dismiss stale approvals*, conversas resolvidas e os checks
  `Python conformance`, `JavaScript conformance (cross-language)` e `JSON
  well-formedness`.
- [ ] Não permitir force pushes nem eliminações de `main`; aplicar a regra aos
  administradores.
- [ ] Em **Settings → Actions → General**, definir *Workflow permissions* como
  **Read repository contents permission** e não permitir que Actions crie ou
  aprove pull requests.
- [ ] Em **Settings → Code security and analysis**, ativar *private
  vulnerability reporting*, secret scanning e push protection (quando
  disponíveis para a conta).
- [ ] Em **Settings → Collaborators**, conceder o menor nível de acesso
  necessário; manter *Admin* só para quem gere definições e segurança.
- [ ] Confirmar que `CODEOWNERS` aponta para o maintainer correto antes de usar
  a opção de exigir revisão por code owner.

## Operação contínua

- [ ] Manter `SECURITY.md` e esta checklist atualizados.
- [ ] Tratar alterações normativas através de issues e pull requests, conforme
  `GOVERNANCE.md` e `CONTRIBUTING.md`.
- [ ] Criar uma release/tag imutável para cada versão publicada; não reescrever
  tags já publicadas.
