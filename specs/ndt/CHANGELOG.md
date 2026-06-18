# NDT Changelog

## [2.0.0] — Draft

### Estrutura e identidade
- Campo `perfil` no cabeçalho: `administrativo_simples`, `impresso_complexo`, `misto` (§2.1)
- Hierarquia: documento → anexos → quadros → elementos
- Caminhos canónicos por `id`, estáveis a reordenações

### Tipos de elemento
- `campo_simples`, `campo_calculado`, `tabela_repetivel`, `grupo`
- Campos comuns a todos os elementos: `descontinuado` e `vigencia` (§4.5)
- Visibilidade e obrigatoriedade condicional via NDT-expr (§5)

### Motor de expressões (NDT-expr)
- Operadores aritméticos, comparação, lógicos, ternário
- Funções de agregação, numéricas, condicionais, de data e texto
- Referências absolutas, relativas (`linha.`) e ao cabeçalho NDT (`impresso.`)
- `hoje()` proibida em NDFs finalizados
- Funções externas: puras, versionadas, auditáveis, declaradas em `funcoes_externas[]` (§6.5)

### Validações cruzadas
- `severidade`: `erro` (bloqueia finalização) ou `aviso` (não bloqueia)

### Layout
- Página: formato, orientação, margens
- `paginas_def[]`: modelos de página com `graficos[]`, `campos[]`, `blocos[]`, `mobilia[]`
- Primitivas gráficas: `linha`, `rectangulo`, `grelha_digitos`, `imagem`, `texto_fixo`, `codigo_barras`, `poligono`, `elipse`, `svg`, `tabela_visual`
- Suporte a `rotacao` e `layer` em qualquer elemento gráfico
- `campos[]`: mecanismo canónico para posicionar campos lógicos do NDF (§8.4)
- Sequenciamento: `unica`, `por_linha`, `conforme_necessario`
- Mobília: `numero_pagina`, `texto_fixo`, `marca_agua`
- Recursos: modo `embebido` (base64) ou `referenciado_por_hash` (§8.9)
- Nota normativa: o NDT não é um formato CAD (§8.3)

### Composição
- `resolver` explícito com `tipo: referencia_documental` — separado do NDT-expr (§9.1)
- Cada documento mantém NDT/NDF próprios; anexos têm de estar finalizados

### Conformidade
- Campos descontinuados marcados com `descontinuado: true`, não removidos
- Layout retroativo apenas com preservação de evidência arquivística
