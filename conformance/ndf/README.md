# Suite de conformidade NDF v1.0.0

Suite oficial de testes de conformidade para implementações do NORMORDIS Document Format.

## Estrutura

```
conformance/ndf/
├── README.md               — este ficheiro
├── valid/                  — NDF-core JSON válidos; implementações conformes DEVEM aceitar todos
└── invalid/                — NDF-core JSON inválidos; implementações conformes DEVEM rejeitar todos
```

## Como usar

### Executor de testes de referência

```bash
# Pré-requisito (jsonschema já incluído na maioria dos ambientes)
pip install jsonschema

# Correr as suites NDF, NDT e NCRTF
python3 tools/validate.py

# Validar um ficheiro específico
python3 tools/validate.py path/to/ndf-core.json

# Apenas casos válidos ou inválidos
python3 tools/validate.py --valid-only
python3 tools/validate.py --invalid-only
```

### Campos de metadados de teste (`_*`)

Os ficheiros JSON nesta suite contêm campos prefixados com `_` para documentação interna (`_comment`, `_expected_error`). Estes campos **não fazem parte do formato NDF-core** e **não devem ser emitidos** por implementações conformes.

O executor remove automaticamente todos os campos `_*` antes de validar — este comportamento é intencional e faz parte da especificação da suite. Implementações externas que integrem estes casos de teste devem aplicar o mesmo filtro.

### Produtor e leitor conformes

Um **produtor NDF** é conforme se gerar documentos que satisfaçam os requisitos
do papel de produtor e sejam aceites como válidos, sem campos `_*`.

Um **leitor NDF** é conforme se:
- Processar sem erro todos os exemplos em `valid/` (após remoção dos campos `_*`)
- Emitir erro e recusar processar todos os exemplos em `invalid/`

A validação estrutural usa `specs/ndf/schemas/ndf-core.schema.json` (JSON Schema Draft 2020-12). Os testes de `invalid/` cobrem também regras semânticas que o schema sozinho não captura (RGPD, formatos de referência, etc.). A definição normativa de conformidade encontra-se em **§9 de `SPEC.md`**.

## Casos de teste

O inventário completo e atualizado de todos os casos — desta e das restantes
suites — está em [`conformance/INDEX.md`](../INDEX.md), **gerado
automaticamente** por `tools/build_conformance_index.py` a partir dos
ficheiros reais e dos respetivos campos `_comment`/`_expected_error`.

Não existe aqui uma tabela manual por decisão deliberada: a versão anterior
deste README documentava 14 de 28 casos, por não acompanhar as adições à
suite (achado F15 da revisão pré-RC). A CI verifica que o índice gerado está
sincronizado com os ficheiros.

```bash
python3 tools/build_conformance_index.py   # regenera conformance/INDEX.md
```

Ao acrescentar um caso novo, preencher `_comment` (casos válidos) ou
`_expected_error` (casos inválidos) — é essa a descrição que aparece no
índice.
