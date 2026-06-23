# Contribuir

Este repositório contém especificações, schemas e vetores de conformidade. As
implementações de referência vivem em repositórios separados.

## Comunicar um problema

Abra uma issue para ambiguidades, contradições, erros de schema, vetores
incorretos, falhas de interoperabilidade ou correções editoriais.

## Propor uma alteração

1. Abra primeiro uma issue com o problema e o caso de uso.
2. Identifique impacto em compatibilidade, segurança, arquivo, acessibilidade e
   proteção de dados.
3. Para alterações normativas, atualize conjuntamente texto, schemas, exemplos,
   testes, rastreabilidade e changelog.
4. Abra um pull request ligado à issue.
5. Declare conflitos de interesse e patentes conhecidas potencialmente
   essenciais à proposta.

## Classes de alteração

- **Major**: alteração incompatível de estrutura ou semântica.
- **Minor**: capacidade opcional compatível.
- **Patch**: correção sem impacto no comportamento observável.

A classificação segue [VERSIONING.md](VERSIONING.md). Chamar “clarificação” a
uma alteração não a torna editorial se modificar uma interpretação conforme.

## Vetores de conformidade

- Um vetor `valid/` DEVE satisfazer schema e regras semânticas.
- Um vetor `invalid/` DEVE isolar, sempre que possível, um único requisito.
- O nome, metadados ou documentação do vetor DEVEM identificar o requisito.
- Resultados dependentes de criptografia, renderização ou ambiente DEVEM fixar
  ferramentas, versões e parâmetros relevantes.

## Língua e estilo

O texto normativo segue
[a política editorial](docs/normalization/EDITORIAL-POLICY.md). Traduções não
podem introduzir requisitos novos.

## Licença e propriedade intelectual

Ao contribuir, o participante aceita os termos de [`LICENSE-SPEC`](LICENSE-SPEC)
para o material abrangido e confirma ter autoridade para disponibilizar a sua
contribuição. Não existe CLA neste momento. A aceitação de uma contribuição não
constitui decisão sobre validade ou essencialidade de patentes.

## Conduta

As discussões devem ser respeitadoras, fundamentadas, rastreáveis e orientadas
à correção técnica e à interoperabilidade.
