# Convenção de Registo de Proveniência de IA (commits)

Define como distinguir, no histórico git, contribuições assistidas por IA de
contribuições humanas diretas. Complementa a política geral em
[AI_USAGE.md](../AI_USAGE.md); em caso de divergência, prevalece a política.

> **Não confundir com** [`normalization/AI-PROVENANCE-GUIDANCE.md`](normalization/AI-PROVENANCE-GUIDANCE.md),
> que trata do bloco `proveniencia_ia` do **formato NDF** — isto é, do uso de IA
> na produção dos *documentos* representados em NDF. Este ficheiro trata do uso
> de IA no **desenvolvimento deste projeto**. Âmbitos distintos.

## 1. Regra geral

| Situação | Autoria | Corpo do commit |
|---|---|---|
| Código gerado ou assistido de forma substantiva | Humano **with** modelo | Prompt + nota de output + revisão humana |
| Revisão ou correção humana sobre output de IA | Humana normal | Referência ao commit de origem |
| Trabalho exclusivamente humano | Humana normal | Formato normal, sem menção a IA |

Não é necessário assinalar a ausência de IA. O silêncio significa autoria
humana; a menção é sempre positiva e explícita.

**Substantivo** significa que o output afeta materialmente o resultado
integrado. Aceitar uma sugestão de completação de uma linha não é substantivo.
Integrar um módulo, um algoritmo ou uma estrutura de dados é.

## 2. Formato — commit assistido por IA

```
Author: Carlos Canuto Costa with Claude Opus 5 <carloscanutocosta@gmail.com>
Date:   <data>

<título curto, imperativo>

Prompt: <prompt integral, ou resumo fiel se for muito extenso>
Output: (este commit) | <descrição do que foi alterado antes de commitar>
Revisão humana: <o que foi verificado ou alterado manualmente antes de aceitar>
```

Notas de aplicação:

- O modelo é indicado com nome e versão exatos. Se mudar a meio de uma série
  de commits, cada commit indica o modelo efetivamente usado.
- `Output: (este commit)` usa-se quando o output foi integrado sem alteração.
  Se houve edição antes do commit, descreve-se a diferença.
- `Revisão humana:` não é opcional e não aceita fórmulas vazias. "Revisto" não
  é revisão; indica-se contra o quê se verificou.

Em git, a autoria conjunta regista-se com:

```
git commit --author="Carlos Canuto Costa with Claude Opus 5 <carloscanutocosta@gmail.com>"
```

## 3. Exemplo — commit assistido

```
Author: Carlos Canuto Costa with Claude Opus 5 <carloscanutocosta@gmail.com>
Date:   Thu Sep 10 2026

Implementar serialização canónica JCS no encoder NDF

Prompt: Implementar serialização JSON canónica conforme RFC 8785 estrito
para o encoder NDF, respeitando a canonicalização exigida em
specs/ndf/SPEC.md §1.3. Não alterar a API pública.
Output: (este commit)
Revisão humana: verificado contra conformance/jcs/vectors.json e
conformance/jcs/numbers.json; corrigida manualmente a normalização de
expoentes, que divergia dos vetores numéricos.
```

## 4. Exemplo — commit humano sobre output de IA

```
Author: Carlos Canuto Costa <carloscanutocosta@gmail.com>
Date:   Fri Sep 11 2026

Corrigir ordenação de chaves em a1b2c3d

Ajusta o output assistido do commit anterior: a ordenação de chaves usava
comparação por code point em vez de unidades de código UTF-16, contrariando
RFC 8785. Detetado por revisão manual, não pela suite.
```

O último período do exemplo é deliberado: quando um defeito escapa aos testes
e é apanhado por revisão humana, regista-se, porque é isso que demonstra que a
revisão existe.

## 5. Quando basta o registo geral

Se a assistência se limitar a documentação, tradução ou testes que não são
usados como evidência de conformidade, basta a descrição geral em
[AI_USAGE.md](../AI_USAGE.md). O registo por commit continua a ser preferível
quando praticável.

Para código de implementação, o registo por commit é a prática do projeto.

## 6. Verificação a posteriori

Os commits assistidos são localizáveis por:

```
git log --author="with Claude" --format="%h %ad %an %s" --date=short
git log --grep="^Prompt:" --format="%h %s"
```

Um terceiro pode assim quantificar a extensão do uso de IA sem depender de
declaração nossa.

## 7. Âmbito temporal

Aplica-se a partir da data em vigor indicada em [AI_USAGE.md](../AI_USAGE.md).
Não se aplica retroativamente ao histórico anterior.
