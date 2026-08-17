# Perfis de conformidade de renderizadores NDT

**Estado:** Draft — revisão pública por abrir

Este documento define perfis de verificação observáveis e independentes da
linguagem. Não impõe um motor de renderização.

Os requisitos de renderizador — `NDT-RENDER-001` a `NDT-RENDER-011` — estão
definidos em [`SPEC.md`](SPEC.md) §9.3. Este documento não os repete: descreve
como são verificados, por perfil de saída, e que corpus sustenta essa
verificação.

## Perfil comum

Aplica-se a qualquer saída. `NDT-RENDER-001` a `NDT-RENDER-003` são verificados
por inspeção do comportamento perante entradas defeituosas — versão não
suportada, referência que não resolve, recurso ausente ou com hash incorreto.
`NDT-RENDER-005` e `NDT-RENDER-006` são verificados pelo relatório de
renderização, que identifica implementação, versão, perfil de saída e
aproximações aplicadas.

`NDT-RENDER-007` a `NDT-RENDER-011` regem o tratamento de dados ausentes,
estrutura mínima de tabela, extravasamento em `fluxo`, espaços de tokens e
resolução de famílias tipográficas; são verificados pelo corpus abaixo, em
qualquer perfil de saída.

## Perfil de saída semântica

HTML, ODF e formatos de fluxo são conformes quando a árvore semântica extraída
corresponde à árvore esperada: títulos, parágrafos, segmentos, marcas, listas,
tabelas, imagens, ligações e ordem de leitura. Não se exige igualdade de pixéis.

## Perfil PDF de layout fixo

Este perfil fixa adicionalmente geometria, coordenadas, overflow, fontes,
substituições, hashes, espaço de cor, ordem de leitura e acessibilidade. Os
testes golden DEVEM comparar:

1. número e caixas das páginas;
2. texto normalizado e ordem de leitura;
3. bounding boxes com tolerância declarada;
4. estrutura tagged PDF e texto alternativo;
5. identidades de fontes e recursos incorporados;
6. relatórios PDF/A e PDF/UA dos subperfis declarados.

Igualdade binária é opcional e a sua declaração só é admissível quando o perfil fixa motor
e ambiente completo de serialização.

## Corpus necessário

- cada primitiva NDT isoladamente;
- overflow multipágina com conteúdo antes e depois de NCRTF;
- listas aninhadas, tabelas e imagens;
- valores opcionais e obrigatórios ausentes;
- inclusão condicional;
- falha de recurso ou hash;
- acessibilidade e texto bidirecional/Unicode;
- pelo menos dois renderizadores ou extratores independentes antes de alegar
  interoperabilidade estável.

O repositório valida atualmente estrutura e referências NDT, mas ainda não
contém todos os resultados golden. Este é um gate de implementação.
