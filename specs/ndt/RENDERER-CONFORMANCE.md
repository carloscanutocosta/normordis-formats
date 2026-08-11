# Perfis de conformidade de renderizadores NDT

**Estado:** Draft — revisão pública por abrir

Este documento define papéis observáveis e independentes da linguagem. Não
impõe um motor de renderização.

## Perfil comum

Todo o renderizador DEVE:

- **NDT-RENDER-001** — verificar versão NDT e referências semânticas antes de renderizar;
- **NDT-RENDER-002** — resolver caminhos relativamente a `NDF-core.documento`;
- **NDT-RENDER-003** — rejeitar recursos obrigatórios ausentes ou com hash incorreto;
- **NDT-RENDER-004** — preservar texto, ordem, ligações, listas, tabelas e texto alternativo NCRTF;
- **NDT-RENDER-005** — comunicar capacidades de saída não suportadas em vez de declarar
  silenciosamente conformidade integral;
- **NDT-RENDER-006** — registar nome e versão do renderizador e perfil de saída num relatório.

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
