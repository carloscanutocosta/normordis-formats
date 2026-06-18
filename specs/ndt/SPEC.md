# Especificação NDT v2.0.0

**NORMORDIS Document Template — Especificação Formal**

Estado: Draft para implementação
Âmbito: formato declarativo para descrever a estrutura, validação, fórmulas, elementos gráficos e layout de qualquer documento institucional — desde impressos fiscais complexos (ex.: Modelo 3 IRS) a documentos administrativos correntes (ofícios, informações, despachos).

## Licenciamento

Esta especificação (texto, estrutura, JSON Schemas e exemplos associados) é disponibilizada sob **CC0 1.0** (domínio público). O objetivo é que qualquer produtor de software para a Administração Pública — open source ou proprietário — possa implementar leitura e renderização de NDT livremente, sem qualquer obrigação contratual ou de licenciamento para com o autor da especificação.

A **implementação de referência** (`normordis-pdf`, bibliotecas Rust) é distribuída sob licença separada (EUPL v1.2), indicada no respetivo repositório. Esta especificação é licenciada separadamente (`LICENSE-SPEC`) precisamente para que a adoção do formato não dependa da licença do código.

---

## 1. Relação com o NDF

- **NDT** = template/schema (esta especificação): descreve estrutura, validação, layout.
- **NDF** = instância de dados preenchidos (spec NDF v1.0.0): contém os valores concretos.
- **Relação**: `normordis-pdf` consome `NDT + NDF → PDF/A`. Validação corre sobre o NDF usando as regras do NDT.

### 1.1 Ligação NDF ↔ NDT

O campo `metadados.tipo_documento_ref` do NDF-core (spec NDF §2.5.2) identifica o tipo de documento e corresponde ao `schema_id` do NDT. O campo `ndt_version_ref` do NDF-core identifica a versão concreta do impresso/template usada no momento da finalização, correspondendo ao par `schema_id@versao_impresso` do NDT (ex.: `modelo3-irs@2026.1`).

| NDF-core | NDT | Significado |
|---|---|---|
| `metadados.tipo_documento_ref` | `schema_id` | Identifica o tipo de documento |
| `ndt_version_ref` | `schema_id@impresso.versao_impresso` | Identifica a versão concreta do template |

### 1.2 Dois papéis temporais do NDT

O NDT desempenha papéis diferentes consoante o estado do NDF:

- **Durante `rascunho`**: o NDT é o motor — fornece estrutura para preenchimento, expressões que calculam campos derivados, condições `visivel_se`/`obrigatorio_se`, e validações cruzadas.
- **Após `finalizado`**: o NDF é autossuficiente (valores materializados, calculados e congelados via JCS/RFC 8785 — ver spec NDF §5). O NDT deixa de ser consultado para cálculo ou validação. O único bloco ainda relevante é `layout` — e mesmo esse só para saber onde posicionar cada valor na página, não o que esse valor é ou como foi obtido.

**Implicação prática**: alterações ao bloco `layout` do NDT podem ser aplicadas retroativamente à renderização de NDFs `finalizado` apenas quando preservem integralmente o conteúdo, a ordem lógica de leitura, os identificadores visuais, os códigos de validação e a rastreabilidade da versão usada na renderização original. Quando a paginação, ordem visual ou evidência arquivística forem relevantes para prova, a renderização original deve ser preservada como artefacto autónomo no NDF ou no core-documental. Alterações a qualquer outra secção do NDT são irrelevantes para NDFs `finalizado`.

---

## 2. Identidade e versionamento

```json
{
  "ndt_version": "2.0.0",
  "schema_id": "modelo3-irs",
  "perfil": "impresso_complexo",
  "impresso": {
    "ano_fiscal": 2026,
    "versao_impresso": "2026.1",
    "emissor": "AT",
    "referencia": "Portaria n.º .../2026"
  }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ndt_version` | Sim | Versão do **formato NDT** (semver). Só muda com alterações ao próprio formato NDT, não ao impresso. |
| `schema_id` | Sim | Identificador estável do tipo de documento (ex.: `modelo3-irs`, `oficio-generico`). Imutável — identifica o tipo, não a versão. |
| `perfil` | Sim | Perfil de complexidade do documento. Ver §2.1. |
| `impresso.versao_impresso` | Sim | Versão do impresso oficial (ex.: `2026.1`). Muda anualmente para impressos fiscais. Alterações anuais ao impresso **não** alteram `ndt_version`. |
| `impresso.ano_fiscal` | Condicional | Obrigatório para impressos fiscais; omitido para documentos administrativos. |
| `impresso.emissor` | Não | Entidade emissora do impresso (ex.: `AT`, `SS`, ou omitido para documentos institucionais genéricos). |
| `impresso.referencia` | Não | Referência legal do impresso (ex.: portaria). |

### 2.1 Perfis de complexidade (`perfil`)

O campo `perfil` declara o nível de complexidade esperado do documento. Não cria dois formatos distintos — define qual o subconjunto de funcionalidades NDT que o template utiliza, permitindo que validadores e renderers apliquem expectativas adequadas.

| Valor | Descrição |
|---|---|
| `"administrativo_simples"` | Documentos de estrutura plana: ofícios, informações, despachos, notificações, requerimentos. Pode omitir anexos, tabelas repetíveis, expressões e funções externas. |
| `"impresso_complexo"` | Impressos fiscais e formulários declarativos: múltiplos anexos, quadros, tabelas repetíveis, grelhas de dígitos, campos calculados, validações cruzadas, funções externas versionadas, composição documental. |
| `"misto"` | Documentos que combinam corpo textual administrativo com secções estruturadas ou formulários embebidos. |

**Regra de versionamento**: `ndt_version` segue o mesmo princípio major/minor da spec NDF §7 — versões minor adicionam campos opcionais sem quebrar leitores existentes; versões major introduzem mudanças incompatíveis.

---

## 3. Hierarquia de estrutura

```
documento (NDT)
└── anexos[]             ← Anexo A, B, G, ... (opcional/repetível)
    └── quadros[]        ← Quadro 4, Quadro 5, ...
        └── elementos[]  ← campo_simples | campo_calculado | tabela_repetivel | grupo | enum
```

Cada nível tem um `id` único no seu âmbito. O **caminho canónico** de um elemento é resolvido por `id` (não por índice numérico no array), tornando os caminhos estáveis a reordenações:

```
anexoG.quadro4.imoveis.valor_realizacao
```

Usado pelo motor de expressões (§6) e como referência entre NDF e NDT. O NDF armazena valores nos mesmos caminhos canónicos.

---

## 4. Tipos de elemento (`elementos[]`)

Todos os elementos têm um campo discriminante obrigatório `"tipo"` que determina a sua estrutura. Valores possíveis: `campo_simples`, `campo_calculado`, `tabela_repetivel`, `grupo`.

### 4.1 `campo_simples`

```json
{
  "tipo": "campo_simples",
  "id": "nif_titular",
  "campo_tipo": "nif",
  "rotulo": "NIF do sujeito passivo",
  "codigo": "01",
  "obrigatorio": true,
  "visivel_se": null,
  "obrigatorio_se": null,
  "restricoes": {}
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `tipo` | Sim | Discriminante: `"campo_simples"` |
| `id` | Sim | Identificador único no âmbito do quadro |
| `campo_tipo` | Sim | Tipo de dado (ver tabela abaixo) |
| `rotulo` | Sim | Texto do rótulo/label do campo |
| `codigo` | Não | Código oficial do campo no impresso (para rastreio/conformidade) |
| `obrigatorio` | Não | Default: `false` |
| `visivel_se` | Não | Expressão booleana (§6); `null` = sempre visível |
| `obrigatorio_se` | Não | Expressão booleana (§6); `null` = obrigatoriedade estática |
| `restricoes` | Não | Restrições específicas do tipo (ver tabela abaixo) |

**Tipos primitivos (`campo_tipo`) e restrições:**

| `campo_tipo` | Restrições suportadas |
|---|---|
| `texto` | `max_len` (int), `padrao` (regex), `maiusculas` (bool) |
| `numero` | `min` (num), `max` (num), `casas_decimais` (int) |
| `inteiro` | `min` (int), `max` (int) |
| `monetario` | `min` (num), `max` (num), `moeda` (string, default `"EUR"`), `casas_decimais` (int, default `2`) |
| `data` | `min` (ISO 8601), `max` (ISO 8601), `formato` (string, default `"YYYY-MM-DD"`) |
| `nif` | `valida_check` (bool, default `true`) — validação de dígito de controlo PT |
| `iban` | `valida_mod97` (bool, default `true`) — validação MOD-97 |
| `booleano` | — |
| `enum` | `valores` (array de `{codigo, rotulo}`) |

**Exemplo com restrições:**

```json
{
  "tipo": "campo_simples",
  "id": "ano_aquisicao",
  "campo_tipo": "inteiro",
  "rotulo": "Ano de aquisição",
  "obrigatorio": true,
  "restricoes": {
    "min": 1900,
    "max": 2099
  }
}
```

**Exemplo de enum:**

```json
{
  "tipo": "campo_simples",
  "id": "afetacao",
  "campo_tipo": "enum",
  "rotulo": "Tipo de afetação",
  "restricoes": {
    "valores": [
      { "codigo": "01", "rotulo": "Habitação própria permanente" },
      { "codigo": "02", "rotulo": "Arrendamento" }
    ]
  }
}
```

### 4.2 `campo_calculado`

Não editável; valor derivado por expressão. Recalculado automaticamente pelo motor de expressões (§6) sempre que os campos de que depende mudam.

```json
{
  "tipo": "campo_calculado",
  "id": "mais_valia",
  "campo_tipo": "monetario",
  "rotulo": "Mais-valia apurada",
  "expressao": "valor_realizacao - (valor_aquisicao * coeficiente) - despesas - encargos",
  "visivel_se": null
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `tipo` | Sim | Discriminante: `"campo_calculado"` |
| `id` | Sim | Identificador único no âmbito do quadro |
| `campo_tipo` | Sim | Tipo de dado do resultado |
| `rotulo` | Sim | Texto do rótulo |
| `expressao` | Sim | Expressão do motor NDT-expr (§6) |
| `visivel_se` | Não | Expressão booleana (§6) |

### 4.3 `tabela_repetivel`

Linhas dinâmicas com schema de colunas. Núcleo para impressos fiscais com conjuntos de dados variáveis.

```json
{
  "tipo": "tabela_repetivel",
  "id": "imoveis",
  "rotulo": "Identificação dos imóveis alienados",
  "min_linhas": 1,
  "max_linhas": 50,
  "linha_id_prefixo": "4001",
  "visivel_se": null,
  "colunas": [
    {
      "id": "freguesia",
      "campo_tipo": "texto",
      "rotulo": "Código de freguesia",
      "obrigatorio": true,
      "restricoes": { "max_len": 6 }
    },
    {
      "id": "valor_realizacao",
      "campo_tipo": "monetario",
      "rotulo": "Valor de realização",
      "obrigatorio": true
    },
    {
      "id": "valor_aquisicao",
      "campo_tipo": "monetario",
      "rotulo": "Valor de aquisição",
      "obrigatorio": true
    },
    {
      "id": "coeficiente",
      "campo_tipo": "numero",
      "rotulo": "Coeficiente de desvalorização",
      "calculado": true,
      "expressao": "coef_desvalorizacao(linha.ano_aquisicao, impresso.ano_fiscal)"
    },
    {
      "id": "mais_valia_linha",
      "campo_tipo": "monetario",
      "rotulo": "Mais-valia da linha",
      "calculado": true,
      "expressao": "linha.valor_realizacao - (linha.valor_aquisicao * linha.coeficiente)"
    }
  ]
}
```

**Colunas calculadas** dentro da tabela referenciam outras colunas **da mesma linha** com prefixo `linha.`. Agregações sobre a tabela (usadas fora dela) usam funções de agregação: `soma(anexoG.quadro4.imoveis.valor_realizacao)`, `contar(anexoG.quadro4.imoveis)`, etc.

### 4.4 `grupo`

Campos agrupados, opcionalmente com exclusividade mútua (checkboxes mutuamente exclusivos).

```json
{
  "tipo": "grupo",
  "id": "regime_tributacao",
  "rotulo": "Regime de tributação",
  "exclusivo": true,
  "visivel_se": null,
  "opcoes": [
    { "id": "englobamento", "rotulo": "Opção pelo englobamento" },
    { "id": "taxa_autonoma", "rotulo": "Tributação autónoma (28%)" }
  ]
}
```

Quando `exclusivo: true`, exactamente uma opção deve estar seleccionada (obrigatoriedade implícita). Quando `exclusivo: false`, qualquer combinação é válida.

### 4.5 Campos comuns a todos os elementos

Qualquer elemento (`campo_simples`, `campo_calculado`, `tabela_repetivel`, `grupo`, bem como `anexos[]` e `quadros[]`) pode declarar:

```json
{
  "descontinuado": false,
  "vigencia": {
    "desde": "2026-01-01",
    "ate": null
  }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `descontinuado` | Não | Default `false`. Quando `true`, o elemento deixou de ser usado em versões novas mas permanece descrito no NDT para leitura retrocompatível de NDFs antigos. |
| `vigencia.desde` | Não | Data de início de validade do elemento (ISO 8601). |
| `vigencia.ate` | Não | Data de fim de validade, ou `null` se ainda vigente. |

Elementos com `descontinuado: true` são ignorados no preenchimento de novos NDFs e nas validações cruzadas de documentos novos, mas permanecem no NDT para garantir que NDFs antigos que os contenham continuam legíveis.

---

## 5. Visibilidade e obrigatoriedade condicional

Qualquer elemento (anexo, quadro, campo, tabela, grupo) aceita os campos opcionais:

```json
{
  "visivel_se": "contar(anexoG.quadro4.imoveis) > 0",
  "obrigatorio_se": "documento.residente_nao_habitual == true"
}
```

- Quando `visivel_se` avalia a `false`, o elemento é **omitido do layout** e as suas regras de validação são **suspensas** — não é erro ter um campo não preenchido se esse campo não está visível.
- `obrigatorio_se` sobrepõe-se a `obrigatorio` quando presente — permite obrigatoriedade dinâmica sem duplicar a definição do campo.
- Ambas as expressões são avaliadas pelo motor NDT-expr (§6), com acesso ao NDF completo.

---

## 6. Motor de expressões (NDT-expr)

Subset declarativo e puro (sem efeitos colaterais, determinístico). Avaliado sobre o NDF no contexto de cada elemento.

### 6.1 Operadores

| Categoria | Operadores |
|---|---|
| Aritmético | `+ - * / %` |
| Comparação | `== != < <= > >=` |
| Lógico | `&& \|\| !` |
| Condicional | `? :` (ternário) |

### 6.2 Literais

Número (`42`, `3.14`), string (`"texto"`), booleano (`true`, `false`), `null`.

### 6.3 Referências

- **Caminho canónico absoluto**: `anexoG.quadro4.imoveis.valor_realizacao` — referencia um campo por caminho completo desde a raiz.
- **Referência relativa (dentro de tabela)**: `linha.valor_realizacao` — referencia uma coluna da mesma linha, só válido em `expressao` de colunas de `tabela_repetivel`.
- **Referência ao cabeçalho NDT**: `impresso.ano_fiscal` — acesso a campos do bloco `impresso` do próprio NDT (ex.: para `coef_desvalorizacao`).

### 6.4 Funções

| Categoria | Função | Descrição |
|---|---|---|
| Agregação | `soma(tabela.coluna)` | Soma todos os valores da coluna na tabela |
| Agregação | `media(tabela.coluna)` | Média aritmética |
| Agregação | `max(tabela.coluna)` | Valor máximo |
| Agregação | `min(tabela.coluna)` | Valor mínimo |
| Agregação | `contar(tabela)` | Número de linhas da tabela |
| Numérico | `arred(x, casas)` | Arredondamento |
| Numérico | `abs(x)` | Valor absoluto |
| Numérico | `teto(x)` | Arredondamento para cima |
| Numérico | `piso(x)` | Arredondamento para baixo |
| Condicional | `se(cond, a, b)` | Equivalente ao ternário `cond ? a : b` |
| Condicional | `coalesce(a, b, ...)` | Primeiro valor não-null |
| Data | `ano(d)` | Extrai o ano de uma data |
| Data | `mes(d)` | Extrai o mês de uma data |
| Data | `dias_entre(d1, d2)` | Número de dias entre duas datas |
| Data | `hoje()` | Data actual (só para rascunhos; proibida em campos de NDFs finalizados) |
| Texto | `comprimento(s)` | Número de caracteres |
| Texto | `concat(a, b, ...)` | Concatenação |
| Tabela | `para_cada(tabela, expressao)` | Avalia expressão para cada linha; retorna `true` se todas forem verdadeiras |

**Nota sobre `hoje()`**: proibida em qualquer expressão cujo resultado seja materializado num NDF `finalizado` — um documento fechado não pode ter valores que mudem com o tempo. Permitida apenas em contexto de rascunho, UX, avisos ou pré-preenchimento transitório.

### 6.5 Funções externas (`funcoes_externas[]`)

Lógica fiscal complexa, tabelas oficiais, coeficientes versionados e regras de domínio não são embebidos no NDT-expr. Devem ser declarados como funções externas — puras, determinísticas, versionadas e auditáveis — registadas num catálogo de funções autorizadas.

```json
{
  "funcoes_externas": [
    {
      "nome": "coef_desvalorizacao",
      "versao": "2026.1",
      "origem": "domain-service-irs",
      "pura": true,
      "auditavel": true
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `nome` | Sim | Nome pelo qual a função é invocada nas expressões NDT-expr |
| `versao` | Sim | Versão da função — registada no NDF quando o valor é materializado |
| `origem` | Sim | Identificador do serviço ou módulo que resolve a função |
| `pura` | Sim | Deve ser `true` — funções externas têm de ser determinísticas para o mesmo conjunto de argumentos |
| `auditavel` | Sim | Deve ser `true` — toda a invocação deve ser auditável e reproduzível |

**Regra**: o renderer não contém regras fiscais nem decisões de negócio. Executa estrutura, expressões NDT-expr e chamadas a funções externas previamente declaradas e autorizadas. Funções externas não declaradas em `funcoes_externas[]` são recusadas pelo motor.

---

## 7. Validações cruzadas

Regras de nível de documento, avaliadas após cálculo. Não bloqueiam edição — produzem feedback inline conforme o padrão UX NORMORDIS (`Novo | Editar → Gravar | Cancelar`, validação mantém modo edição com feedback inline).

```json
{
  "validacoes": [
    {
      "id": "soma_quadro5",
      "regra": "anexoG.quadro5.total_mais_valias == soma(anexoG.quadro4.imoveis.mais_valia_linha)",
      "mensagem": "O total do Quadro 5 deve igualar a soma das mais-valias do Quadro 4.",
      "severidade": "erro"
    },
    {
      "id": "data_aquisicao_anterior",
      "regra": "para_cada(anexoG.quadro4.imoveis, linha.data_aquisicao < linha.data_realizacao)",
      "mensagem": "A data de aquisição tem de ser anterior à de realização.",
      "severidade": "erro"
    },
    {
      "id": "aviso_valor_elevado",
      "regra": "soma(anexoG.quadro4.imoveis.valor_realizacao) < 10000000",
      "mensagem": "Valor total de realização superior a 10M€ — confirmar valores introduzidos.",
      "severidade": "aviso"
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Identificador único da validação |
| `regra` | Sim | Expressão booleana NDT-expr |
| `mensagem` | Sim | Texto apresentado ao utilizador quando a regra falha |
| `severidade` | Sim | `"erro"` (bloqueia finalização) \| `"aviso"` (não bloqueia) |

---

## 8. Layout (renderização PDF)

O bloco `layout` é opcional — sem ele, `normordis-pdf` aplica layout automático. Quando presente, permite controlo preciso sobre posicionamento, elementos gráficos, e paginação.

O bloco `layout` mantém-se **separado da estrutura lógica** para permitir múltiplos renderers do mesmo NDT (ex.: um renderer PDF e um renderer HTML partilham a mesma estrutura lógica mas layouts distintos).

### 8.1 Configuração de página

```json
{
  "layout": {
    "formato": "A4",
    "orientacao": "portrait",
    "margens": { "topo": 20, "fundo": 20, "esq": 15, "dir": 15 }
  }
}
```

`formato`: `"A4"` | `"A3"` | `"Letter"` | `{ "largura": num, "altura": num }` (mm).
`orientacao`: `"portrait"` | `"landscape"`.
`margens`: em milímetros.

### 8.2 Definições de página (`paginas_def[]`)

A unidade fundamental do layout é a **definição de página** (`pagina_def`). Cada página de um impresso multi-página (rosto, Anexo G pág. 1, Anexo G pág. 2…) ou cada variante de página (primeira página com cabeçalho completo vs. páginas seguintes só com rodapé) é uma `pagina_def` própria. Não existe "página genérica repetida" como conceito base — repetição é controlada por `sequencia[]` (§8.6).

Cada `pagina_def` pode conter quatro tipos de elementos, todos com o mesmo sistema de coordenadas (milímetros, origem `(0,0)` no canto superior-esquerdo da área útil):

- `graficos[]` — elementos visuais puros (§8.3)
- `campos[]` — campos de dados do NDF posicionados (§8.4)
- `blocos[]` — referências a secções/tabelas lógicas (§8.5)
- `mobilia[]` — elementos fixos de página (numeração, cabeçalhos/rodapés) (§8.7)

```json
{
  "paginas_def": [
    {
      "id": "rosto",
      "graficos": [],
      "campos": [],
      "blocos": [],
      "mobilia": []
    }
  ]
}
```

### 8.3 Elementos gráficos (`graficos[]`)

Elementos puramente visuais — sem correspondência a campos lógicos do NDF (excepto `grelha_digitos`, que liga a um caminho canónico). Para posicionar valores de campos lógicos na página, usar `campos[]` (§8.4).

Todos os elementos gráficos partilham o campo discriminante `"tipo"` e o sistema de coordenadas mm (origem área útil da `pagina_def`).

> **Nota normativa**: o NDT não é um formato CAD nem uma linguagem de desenho genérica. As primitivas gráficas existem apenas para suportar a representação de documentos institucionais. Novas primitivas devem ser introduzidas apenas quando representem padrões recorrentes de documentação administrativa.

#### 8.3.1 `linha`

```json
{
  "tipo": "linha",
  "de": { "x": 15, "y": 40 },
  "para": { "x": 195, "y": 40 },
  "espessura": 0.3,
  "cor": "#000000",
  "estilo": "solido"
}
```

`estilo`: `"solido"` | `"tracejado"` | `"ponteado"`.

#### 8.3.2 `rectangulo`

```json
{
  "tipo": "rectangulo",
  "posicao": { "x": 15, "y": 45 },
  "largura": 180,
  "altura": 30,
  "preenchimento": "none",
  "contorno": { "espessura": 0.3, "cor": "#000000" },
  "raio_canto": 0
}
```

`preenchimento`: `"none"` | cor hex (`"#RRGGBB"`).
`raio_canto`: milímetros; `0` = ângulos rectos.

#### 8.3.3 `grelha_digitos`

Primitiva específica para impressos fiscais — caixas individuais por carácter (NIFs, datas, códigos). Encapsula o padrão "uma caixa por carácter" sem que cada caixa seja um elemento separado, mantendo a ligação ao campo lógico para validação de comprimento.

```json
{
  "tipo": "grelha_digitos",
  "referencia": "anexoG.quadro4.imoveis.freguesia",
  "posicao": { "x": 60, "y": 52 },
  "num_caixas": 6,
  "largura_caixa": 5,
  "altura_caixa": 6,
  "espacamento": 0.5,
  "cor_contorno": "#000000",
  "espessura_contorno": 0.3
}
```

`referencia`: caminho canónico do campo de onde vêm os caracteres. O renderer distribui cada carácter numa caixa; o motor de validação sabe que este campo aceita no máximo `num_caixas` caracteres.

#### 8.3.4 `imagem`

```json
{
  "tipo": "imagem",
  "referencia_recurso": "logo-at.svg",
  "posicao": { "x": 15, "y": 10 },
  "largura": 30,
  "altura": 12,
  "manter_proporcao": true
}
```

`referencia_recurso`: identificador de um recurso declarado em `layout.recursos[]` (§8.9).
`manter_proporcao`: se `true`, `largura` e `altura` definem a caixa de delimitação e a imagem é escalada proporcionalmente dentro dela.

#### 8.3.5 `texto_fixo`

Texto estático, não proveniente do NDF — títulos, legendas, rótulos de secção.

```json
{
  "tipo": "texto_fixo",
  "conteudo": "MODELO 3",
  "posicao": { "x": 150, "y": 12 },
  "fonte": {
    "familia": "Helvetica",
    "tamanho": 14,
    "peso": "bold",
    "estilo": "normal",
    "cor": "#000000"
  },
  "alinhamento": "esquerda"
}
```

`conteudo` pode conter placeholders do cabeçalho NDT: `{{impresso.ano_fiscal}}`, `{{schema_id}}`.
`peso`: `"normal"` | `"bold"`.
`estilo`: `"normal"` | `"italico"`.
`alinhamento`: `"esquerda"` | `"centro"` | `"direita"`.

#### 8.3.6 `codigo_barras`

```json
{
  "tipo": "codigo_barras",
  "formato": "qrcode",
  "conteudo": "{{sistema.url_validacao}}/{{ndf.codigo_validacao}}",
  "posicao": { "x": 170, "y": 270 },
  "largura": 25,
  "altura": 25,
  "nivel_correcao": "M"
}
```

`formato`: `"qrcode"` | `"code128"` | `"ean13"`.
`conteudo`: string com placeholders — `{{sistema.url_validacao}}` e `{{ndf.codigo_validacao}}` são placeholders de sistema resolvidos pelo renderer (não pelo motor NDT-expr).
`nivel_correcao` (só QR): `"L"` | `"M"` | `"Q"` | `"H"`.

Este é o elemento que gera o **código de validação visual** obrigatório em todos os documentos NORMORDIS (ver spec NDF §...) — deve estar presente no rodapé de pelo menos uma `pagina_def` de cada NDT.

#### 8.3.7 Sumário de tipos gráficos

| `tipo` | Descrição | Liga ao NDF? |
|---|---|---|
| `linha` | Linha recta com cor, espessura e estilo | Não |
| `rectangulo` | Rectângulo com preenchimento e contorno | Não |
| `grelha_digitos` | Caixas por carácter (NIFs, códigos) | Sim (valor) |
| `imagem` | Imagem/logótipo de recurso | Não |
| `texto_fixo` | Texto estático ou com placeholders NDT | Não |
| `codigo_barras` | QR code ou código de barras | Sim (código validação) |
| `poligono` | Forma arbitrária por vértices | Não |
| `elipse` | Círculo ou elipse | Não |
| `svg` | Gráfico vetorial completo de recurso | Não |
| `tabela_visual` | Grelha de linhas e colunas fixas | Não |

#### 8.3.8 `poligono`

Forma arbitrária composta por segmentos de reta — triângulos, setas, formas personalizadas.

```json
{
  "tipo": "poligono",
  "pontos": [
    { "x": 10, "y": 10 },
    { "x": 30, "y": 10 },
    { "x": 20, "y": 25 }
  ],
  "preenchimento": "none",
  "contorno": { "espessura": 0.3, "cor": "#000000" }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `pontos` | Sim | Lista ordenada de vértices (mm). O último ponto liga automaticamente ao primeiro. |
| `preenchimento` | Não | `"none"` ou cor hex. |
| `contorno` | Não | Estilo do contorno. |

#### 8.3.9 `elipse`

Círculo ou elipse. Quando `raio_x == raio_y`, a figura é um círculo.

```json
{
  "tipo": "elipse",
  "centro": { "x": 100, "y": 80 },
  "raio_x": 15,
  "raio_y": 10,
  "preenchimento": "none",
  "contorno": { "espessura": 0.3, "cor": "#000000" }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `centro` | Sim | Centro geométrico (mm). |
| `raio_x` | Sim | Raio horizontal (mm). |
| `raio_y` | Sim | Raio vertical (mm). |
| `preenchimento` | Não | `"none"` ou cor hex. |
| `contorno` | Não | Estilo do contorno. |

#### 8.3.10 Rotação (`rotacao`)

Qualquer elemento gráfico pode declarar um campo `rotacao` (graus, sentido horário). O renderer pode aceitar qualquer valor numérico; valores recomendados: `0`, `90`, `180`, `270`.

```json
{
  "tipo": "texto_fixo",
  "conteudo": "Reservado aos serviços",
  "posicao": { "x": 180, "y": 100 },
  "rotacao": 90,
  "fonte": { "familia": "Helvetica", "tamanho": 8 }
}
```

#### 8.3.11 Camadas (`layer`)

Qualquer elemento gráfico pode declarar uma camada de renderização. Valor por omissão: `"content"`.

| Valor | Ordem | Utilização típica |
|---|---|---|
| `"background"` | 1.º | Fundo do impresso |
| `"content"` | 2.º | Caixas, linhas, grelhas |
| `"foreground"` | 3.º | Dados preenchidos |
| `"overlay"` | 4.º | Marcas de água, selos |

```json
{
  "tipo": "imagem",
  "referencia_recurso": "marca-agua.svg",
  "posicao": { "x": 0, "y": 0 },
  "largura": 210,
  "altura": 297,
  "layer": "overlay"
}
```

#### 8.3.12 `svg`

Gráfico vetorial completo proveniente de um recurso declarado em `layout.recursos[]` (§8.9). Independente de resolução; pode ser usado como fundo completo de página.

```json
{
  "tipo": "svg",
  "referencia_recurso": "modelo3-fundo.svg",
  "posicao": { "x": 0, "y": 0 },
  "largura": 210,
  "altura": 297,
  "layer": "background"
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `referencia_recurso` | Sim | Identificador do recurso SVG (§8.9). |
| `posicao` | Sim | Origem (mm). |
| `largura` | Sim | Largura renderizada (mm). |
| `altura` | Sim | Altura renderizada (mm). |

#### 8.3.13 `tabela_visual`

Primitiva gráfica para desenhar grelhas de linhas e colunas fixas — evita a necessidade de declarar manualmente dezenas de linhas e rectângulos.

```json
{
  "tipo": "tabela_visual",
  "posicao": { "x": 15, "y": 50 },
  "largura": 180,
  "altura_linha": 6,
  "num_linhas": 10,
  "colunas": [30, 50, 40, 60],
  "contorno": { "espessura": 0.3, "cor": "#000000" }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `num_linhas` | Sim | Número de linhas da grelha. |
| `colunas` | Sim | Array de larguras de coluna (mm); a soma deve igualar `largura`. |
| `altura_linha` | Sim | Altura de cada linha (mm). |
| `contorno` | Não | Estilo das linhas da grelha. |

### 8.4 Campos posicionados (`campos[]`)

Mecanismo canónico para posicionar valores de campos lógicos do NDF numa posição absoluta na página — para layouts de impressos onde cada campo tem coordenadas fixas definidas pelo impresso oficial, ou quando o renderer precisa de aplicar lógica de edição (modo de preenchimento interactivo).

```json
{
  "campos": [
    {
      "referencia": "documento.numero",
      "posicao": { "x": 120, "y": 30 },
      "largura": 60,
      "altura": 7,
      "fonte": { "familia": "Helvetica", "tamanho": 10 },
      "alinhamento": "esquerda",
      "preenchimento_fundo": "none"
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `referencia` | Sim | Caminho canónico do campo no NDF. O renderer escreve o valor nesta posição. |
| `posicao` | Sim | Coordenadas de origem (mm). |
| `largura` | Sim | Largura da caixa de texto (mm). |
| `altura` | Sim | Altura da caixa de texto (mm). |
| `fonte` | Não | Estilo de fonte (§8.8). |
| `alinhamento` | Não | `"esquerda"` \| `"centro"` \| `"direita"`. Default: `"esquerda"`. |
| `preenchimento_fundo` | Não | `"none"` ou cor hex. |

### 8.5 Blocos lógicos (`blocos[]`)

Referência a uma secção ou tabela lógica do NDT, cujo layout interno (colunas, larguras, espaçamento de linhas) é determinado pelo `normordis-pdf` com base na estrutura do NDT e nas dimensões disponíveis.

```json
{
  "blocos": [
    {
      "referencia": "anexoG.quadro4",
      "tipo": "tabela",
      "posicao": { "x": 15, "y": 50 },
      "largura": 180,
      "repete_cabecalho": true
    },
    {
      "referencia": "corpo",
      "tipo": "corpo",
      "posicao": { "x": 15, "y": 60 },
      "largura": 180
    }
  ]
}
```

`tipo`: `"tabela"` | `"quadro"` | `"corpo"` | `"cabecalho"` | `"rodape"`.

### 8.6 Sequenciamento e repetição (`sequencia[]`)

`paginas_def[]` descreve **modelos** de página, não a sequência final do documento. `sequencia[]` ordena-os e controla instâncias:

```json
{
  "sequencia": [
    {
      "pagina_def": "rosto",
      "repeticao": "unica"
    },
    {
      "pagina_def": "anexoG_pag1",
      "repeticao": "conforme_necessario",
      "fonte_overflow": "anexoG.quadro4.imoveis",
      "linhas_por_pagina": 8
    },
    {
      "pagina_def": "anexoG_pag_final",
      "repeticao": "unica"
    }
  ]
}
```

| `repeticao` | Comportamento |
|---|---|
| `"unica"` | A `pagina_def` aparece exactamente uma vez |
| `"por_linha"` | Uma instância por linha de `tabela_repetivel` referenciada em `fonte_overflow` |
| `"conforme_necessario"` | Repete enquanto `fonte_overflow` tiver linhas não colocadas; cada instância recebe até `linhas_por_pagina` |

**Exemplo: primeira página diferente (documentos administrativos)**

O padrão "primeira página com cabeçalho institucional completo, páginas seguintes só com rodapé" é expresso com duas `paginas_def` e uma `sequencia`:

```json
{
  "paginas_def": [
    {
      "id": "oficio_pag1",
      "graficos": [
        {
          "tipo": "imagem",
          "referencia_recurso": "brasao-republica.svg",
          "posicao": { "x": 15, "y": 10 },
          "largura": 25,
          "altura": 25,
          "manter_proporcao": true
        }
      ],
      "blocos": [
        { "referencia": "cabecalho", "tipo": "cabecalho", "posicao": { "x": 45, "y": 10 }, "largura": 150 },
        { "referencia": "corpo", "tipo": "corpo", "posicao": { "x": 15, "y": 60 }, "largura": 180 }
      ],
      "mobilia": [
        {
          "tipo": "numero_pagina",
          "formato": "Pág. {n}/{total}",
          "posicao": { "x": 180, "y": 285 },
          "fonte": { "familia": "Helvetica", "tamanho": 8 }
        }
      ]
    },
    {
      "id": "oficio_pag_seguinte",
      "blocos": [
        { "referencia": "corpo", "tipo": "corpo", "posicao": { "x": 15, "y": 15 }, "largura": 180 }
      ],
      "mobilia": [
        {
          "tipo": "numero_pagina",
          "formato": "Pág. {n}/{total}",
          "posicao": { "x": 180, "y": 285 },
          "fonte": { "familia": "Helvetica", "tamanho": 8 }
        }
      ]
    }
  ],
  "sequencia": [
    { "pagina_def": "oficio_pag1", "repeticao": "unica" },
    { "pagina_def": "oficio_pag_seguinte", "repeticao": "conforme_necessario", "fonte_overflow": "corpo" }
  ]
}
```

### 8.7 Mobília de página (`mobilia[]`)

Elementos fixos de uma `pagina_def` específica — cada `pagina_def` tem a sua própria `mobilia`, pelo que páginas diferentes podem ter numerações/cabeçalhos diferentes.

```json
{
  "mobilia": [
    {
      "tipo": "numero_pagina",
      "formato": "Página {n} de {total}",
      "posicao": { "x": 180, "y": 285 },
      "fonte": { "familia": "Helvetica", "tamanho": 8, "cor": "#666666" }
    },
    {
      "tipo": "texto_fixo",
      "conteudo": "Modelo 3 — {{impresso.ano_fiscal}}",
      "posicao": { "x": 15, "y": 285 },
      "fonte": { "familia": "Helvetica", "tamanho": 8, "cor": "#666666" }
    },
    {
      "tipo": "marca_agua",
      "conteudo": "RASCUNHO",
      "opacidade": 0.15,
      "angulo": 45,
      "fonte": { "familia": "Helvetica", "tamanho": 60, "peso": "bold", "cor": "#FF0000" }
    }
  ]
}
```

`tipo` de mobília: `"numero_pagina"` | `"texto_fixo"` | `"marca_agua"`.
A `"marca_agua"` é renderizada apenas quando o NDF está em estado `rascunho` — o renderer omite-a automaticamente em NDFs `finalizado`.

### 8.8 Fontes

```json
{
  "fonte": {
    "familia": "Helvetica",
    "tamanho": 10,
    "peso": "normal",
    "estilo": "normal",
    "cor": "#000000"
  }
}
```

`familia`: nome da fonte — o renderer deve suportar pelo menos `"Helvetica"`, `"Times"`, `"Courier"` (fontes standard PDF). Fontes adicionais são declaradas como recursos (§8.9).
`peso`: `"normal"` | `"bold"`.
`estilo`: `"normal"` | `"italico"`.

### 8.9 Recursos (`recursos[]`)

Imagens e fontes referenciadas no layout são declaradas em `recursos[]`. Cada recurso pode ser **embebido** diretamente no NDT (template autossuficiente) ou **referenciado por hash** (recurso reside no core-documental ou blob storage controlado, mantendo o NDT leve).

#### Modo `embebido`

```json
{
  "id": "logo-at.svg",
  "tipo": "svg",
  "modo": "embebido",
  "dados": "base64:PHN2ZyB4bWxucy4uLg=="
}
```

#### Modo `referenciado_por_hash`

```json
{
  "id": "brasao-republica.svg",
  "tipo": "svg",
  "modo": "referenciado_por_hash",
  "hash_sha256": "abc123...",
  "content_type": "image/svg+xml",
  "origem": "core-documental"
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Identificador único — referenciado em `referencia_recurso` nos elementos gráficos. |
| `tipo` | Sim | `"svg"` \| `"png"` \| `"jpeg"` \| `"fonte_ttf"` \| `"fonte_otf"`. |
| `modo` | Sim | `"embebido"` \| `"referenciado_por_hash"`. |
| `dados` | Condicional | Conteúdo base64 (prefixo `"base64:"`). Obrigatório quando `modo == "embebido"`. |
| `hash_sha256` | Condicional | Hash SHA-256 do recurso. Obrigatório quando `modo == "referenciado_por_hash"`. |
| `content_type` | Condicional | MIME type do recurso. Obrigatório quando `modo == "referenciado_por_hash"`. |
| `origem` | Não | Identificador da fonte do recurso (ex.: `"core-documental"`). Informativo. |
| `familia` | Condicional | Nome da família de fonte. Obrigatório para `tipo == "fonte_ttf"` ou `"fonte_otf"`. |

**Escolha do modo**: usar `"embebido"` quando o NDT deve ser autossuficiente (distribuição standalone, ausência de infraestrutura); usar `"referenciado_por_hash"` quando os recursos vivem em infraestrutura controlada e o NDT deve manter-se compacto.

---

## 9. Composição de documentos (`composicao[]`)

Permite que um documento principal (ofício, notificação) seja entregue junto com anexos (outros NDFs/NDTs) como um único PDF/A — sem fundir as estruturas lógicas.

```json
{
  "composicao": [
    {
      "id": "anexo_modelo3_anexoG",
      "schema_id": "modelo3-irs-anexoG",
      "resolver": {
        "tipo": "referencia_documental",
        "expressao": "{{numero_processo}}/anexoG"
      },
      "posicao": "apos",
      "apos_bloco": null,
      "obrigatorio": true
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Identificador único desta composição |
| `schema_id` | Sim | `schema_id` do NDT do documento a anexar |
| `resolver` | Sim | Resolver explícito para localizar o NDF a anexar (ver §9.1) |
| `posicao` | Sim | `"antes"` \| `"apos"` \| `"apos_bloco"` |
| `apos_bloco` | Condicional | ID do bloco após o qual inserir (quando `posicao == "apos_bloco"`) |
| `obrigatorio` | Não | Default `false`. Se `true`, falha de resolução bloqueia o fecho do documento principal. |

### 9.1 Resolver de composição

O `resolver` separa a resolução documental (localizar outro NDF) do cálculo interno (NDT-expr). São dois planos distintos.

```json
{
  "resolver": {
    "tipo": "referencia_documental",
    "expressao": "{{numero_processo}}/anexoG"
  }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `tipo` | Sim | `"referencia_documental"` — único tipo suportado nesta versão |
| `expressao` | Sim | Template de referência com placeholders de campos do NDF principal (notação `{{caminho}}`). Resolvido pelo core-documental, não pelo motor NDT-expr. |

**Regra**: placeholders em `resolver.expressao` são resolvidos pelo core-documental com os valores do NDF principal no momento do fecho. Não são expressões NDT-expr — não suportam operadores aritméticos, funções ou condicionais.

### 9.2 Regras

- Cada documento mantém o seu NDT/NDF próprios — não há "schema combinado".
- No momento do fecho do documento principal, cada `ndf_ref` é resolvido e o NDF do anexo **tem de estar também `finalizado`**. Um documento finalizado não pode depender de um anexo em rascunho.
- O NDF principal regista `schema_id`, `ndf_id`, `ndf_hash` e `pdf_hash` de cada anexo resolvido (para verificação de integridade da composição — cada componente é verificável isoladamente).
- A `mobilia` de uma `pagina_def` do documento principal **não** se propaga aos PDFs dos documentos anexados — cada um mantém a sua própria sequência de páginas.

---

## 10. Conformidade e migração

- **Caminhos canónicos estáveis**: entre versões de `versao_impresso`, os `id` de campos existentes não são renomeados — garantia de que NDFs antigos continuam legíveis com NDTs novos.
- **Campos descontinuados**: campos removidos num ano são marcados `"descontinuado": true` em vez de apagados (ver §4.5), preservando a capacidade de ler NDFs antigos.
- **Separação entre lógica declarativa e lógica de domínio**: toda a lógica declarativa parametrizável vive no NDT-expr; funções de domínio complexas (tabelas fiscais, coeficientes versionados, regras específicas) são resolvidas por funções externas puras, versionadas e auditáveis, declaradas em `funcoes_externas[]` (§6.5). O renderer é um executor puro — não contém regras fiscais nem decisões de negócio.
- **Alterações de layout retroativas apenas com preservação de evidência**: conforme §1.2, alterações ao bloco `layout` só podem ser aplicadas retroativamente se preservarem integralmente conteúdo, ordem de leitura, identificadores visuais, códigos de validação e rastreabilidade da versão original.
- **Resolução documental separada de cálculo**: a composição de documentos usa `resolver` explícito (§9.1), não expressões NDT-expr — os dois planos não se misturam.

---

## 11. Glossário

| Termo | Significado |
|---|---|
| NDT | NORMORDIS Document Template — template/schema declarativo (este formato) |
| NDF | NORMORDIS Document Format — instância de dados preenchidos (spec NDF v1.0.0) |
| `schema_id` | Identificador estável do tipo de documento no NDT; corresponde a `tipo_documento_ref` no NDF |
| `versao_impresso` | Versão do impresso/template concreto; parte de `ndt_version_ref` no NDF |
| NDT-expr | Motor de expressões declarativo e puro do NDT (§6) |
| `pagina_def` | Definição de página — modelo de página instanciado pela `sequencia[]` |
| `grafico` | Elemento visual puro de uma `pagina_def` (linha, rectângulo, imagem, etc.) |
| `grelha_digitos` | Primitiva gráfica de caixas por carácter, ligada a um campo do NDF |
| `codigo_barras` | Primitiva gráfica QR/barras, usada para código de validação NORMORDIS |
| Caminho canónico | Referência estável a um campo por `id` (`anexoG.quadro4.imoveis.valor`) |
| Composição | Mecanismo de entrega conjunta de documentos independentes num único PDF/A |
| `perfil` | Nível de complexidade do NDT: `administrativo_simples`, `impresso_complexo`, ou `misto` (§2.1) |
| `funcoes_externas[]` | Catálogo de funções externas declaradas no NDT — puras, versionadas e auditáveis (§6.5) |
| `resolver` | Mecanismo explícito de localização de um NDF externo na composição documental (§9.1) |
| `descontinuado` | Campo de elemento que indica que este deixou de ser usado em versões novas (§4.5) |
