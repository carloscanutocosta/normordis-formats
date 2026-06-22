# Governance

**Estado:** política provisória aplicável enquanto o projecto não for entregue
a uma Comissão Técnica de Normalização.

## Princípios

- As especificações são soberanas e independentes de qualquer implementação.
- Qualquer fornecedor, organização pública ou projecto open source pode implementar
  estas especificações sem dependência das implementações de referência NORMORDIS.
- As alterações às especificações seguem uma política de versionamento (ver [VERSIONING.md](VERSIONING.md)).
- Integridade técnica, autenticidade, assinatura jurídica e apresentação são
  conceitos distintos e não podem ser alterados por mera correcção editorial.
- Nenhuma implementação de referência tem autoridade para contradizer o texto
  normativo, schemas e vectores de conformidade publicados.

## Papéis

- **Maintainers:** gerem propostas e releases; não podem declarar conformidade
  sem evidência produzida pela suite pública.
- **Editors:** mantêm texto, schemas, exemplos e testes sincronizados.
- **Registry stewards:** aprovam identificadores e asseguram que versões
  publicadas permanecem resolúveis e imutáveis.
- **Reviewers externos:** especialistas de arquivo, segurança, acessibilidade e
  direito chamados para alterações no respectivo domínio.

Uma pessoa pode acumular papéis, mas uma alteração normativa não deve ser
aprovada apenas pelo seu autor.

## Processo de alteração

1. A proposta identifica problema, âmbito e compatibilidade.
2. Alterações normativas incluem texto, schema e casos de conformidade.
3. Pelo menos um maintainer diferente do autor revê a proposta.
4. Alterações criptográficas, jurídicas ou arquivísticas exigem revisão de um
   especialista do domínio antes de release estável.
5. A decisão e alternativas rejeitadas são registadas num ADR ou na proposta.

## Releases e congelamento

- Um release estável exige schemas válidos, exemplos válidos, suite integral
  verde e um `.ndfpkg` verificável end-to-end.
- Artefactos de uma versão estável são imutáveis. Correcções comportamentais
  originam nova versão; ficheiros publicados não são substituídos in-place.
- Identificadores e URLs de registry publicados nunca são reciclados.

## Conformidade

O projecto publica testes e vectores, mas não concede certificação formal. Uma
declaração de conformidade deve indicar formato, versão, papel (produtor,
leitor, renderer ou verificador), perfil e versão da suite utilizada.

## Normalização futura

Quando uma Comissão Técnica competente assumir o trabalho, as suas regras de
consenso, votação e manutenção prevalecem. A migração deve preservar histórico,
licença aberta, issues, ADRs e vectores de conformidade.
