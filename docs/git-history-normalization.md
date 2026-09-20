# Normalização histórica de autoria — 2026-09-19

Decisão humana: pedido explícito de Carlos Canuto Costa para autoria Git humana
com assistência de IA declarada, sem alterar conteúdo funcional ou inventar
revisões. A normalização foi executada com assistência de Codex (GPT-6; variante
exata não disponibilizada na sessão).

Cada árvore histórica foi preservada byte a byte (mesmo identificador Git).
Os modelos anteriormente indicados na autoria ou em trailers passaram para
`AI assistance`. Os prompts, notas de output e declarações históricas de revisão
foram preservados como registos, sem os certificar novamente. Versões de modelos
são as declaradas no histórico, não uma validação externa da sua identificação.

O [mapa completo](history-commit-map.tsv) permite resolver referências aos SHA
antigos, incluindo referências abreviadas únicas em documentação ou mensagens.
Não se reescreveram decisões normativas nem se inferiu ausência de IA nos
commits sem declaração. Quando a divisão do trabalho não é demonstrável,
registou-se explicitamente a incerteza. A autoria normalizada segue a atribuição
de responsabilidade autorizada pelo titular; não prova redação humana exclusiva.

Os bundles originais e o relatório operacional externo preservam metadados,
assinaturas, anotações de tags e os registos anteriores. Assinaturas de commits
reescritos deixam de ser válidas e não foram reproduzidas como se o fossem.
As datas originais foram mantidas. Tags anotadas conservam anotação e tagger,
mas o seu objeto muda para apontar para o commit normalizado.

A inspeção e os testes feitos pelo agente são verificações automatizadas,
não revisão humana. A declaração de revisão fornecida pelo responsável consta do commit
documental; não se acrescentam verificações humanas não declaradas.

## Novas assinaturas — 2026-09-20

Por pedido explícito do responsável, apenas os 18 commits deste
repositório que tinham assinatura foram novamente assinados com a chave SSH
do servidor. São assinaturas novas da normalização, não recriações das
assinaturas GitHub nem prova de revisão humana histórica. Nos commits
assinados, o committer passou para Carlos Canuto Costa, mantendo a data
histórica; a data desta operação é registada aqui. Mensagens, árvores e datas
foram preservadas, assim como anotações das tags. Os descendentes receberam
novos SHA sem assinatura adicional. A verificação criptográfica local passou;
o reconhecimento no GitHub depende de registar esta chave pública como
chave de assinatura. Não foi feito push ou registo de chave no GitHub.
