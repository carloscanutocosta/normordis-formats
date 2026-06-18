# NDF Conformance Test Suite v1.0.0

Suite oficial de testes de conformidade para implementações do NORMORDIS Document Format.

## Estrutura

```
conformance/ndf/
├── README.md               — este ficheiro
├── valid/                  — NDF-core JSON válidos; implementações conformes DEVEM aceitar todos
└── invalid/                — NDF-core JSON inválidos; implementações conformes DEVEM rejeitar todos
```

## Como usar

Um **produtor NDF** é conforme se:
- Gerar documentos estruturalmente equivalentes aos exemplos em `valid/`
- Rejeitar inputs com as falhas descritas em `invalid/`

Um **leitor NDF** é conforme se:
- Processar sem erro todos os exemplos em `valid/`
- Emitir erro e recusar processar todos os exemplos em `invalid/`

A validação estrutural usa o schema em `specs/ndf/schema/ndf-core.schema.json`. Os testes de `invalid/` cobrem também regras semânticas que o JSON Schema sozinho não captura.

## Casos de teste

### Válidos

| Ficheiro | O que valida |
|---|---|
| `valid/oficio-qualificado.json` | Caso base — ofício com assinatura qualificada, dados pessoais presentes, todos os campos obrigatórios |
| `valid/despacho-avancado.json` | Despacho com assinatura avançada, sem dados pessoais |
| `valid/registo-interno-sem-assinatura.json` | Documento interno com `nivel_assinatura: "nenhuma"`, conservação permanente |
| `valid/versao-substituicao.json` | NDF que substitui um anterior (campos `versao_anterior`/`hash_anterior` no envelope) |

### Inválidos

| Ficheiro | Regra violada | Secção |
|---|---|---|
| `invalid/missing-nivel-assinatura.json` | Campo obrigatório `nivel_assinatura` ausente | §2.2, §5.1 |
| `invalid/invalid-nivel-assinatura.json` | `nivel_assinatura` com valor fora do enum | §2.10.1 |
| `invalid/missing-ndf-id.json` | Campo obrigatório `ndf_id` ausente | §2.3 |
| `invalid/invalid-uuid.json` | `ndf_id` não é UUID v4 válido | §2.3 |
| `invalid/invalid-estado.json` | `estado` com valor fora do enum | §2.4 |
| `invalid/missing-tipo-documento-ref.json` | `metadados.tipo_documento_ref` ausente | §2.7.2 |
| `invalid/dados-pessoais-sem-base-legal.json` | `contem_dados_pessoais: true` sem `base_legal_conservacao` | §2.7.2, §1.6 |
| `invalid/invalid-tipo-classificacao-ref.json` | `tipo_classificacao_ref` não segue formato `<instrumento>/<codigo>` | §3.2.1 |
| `invalid/invalid-ndt-version-ref.json` | `ndt_version_ref` não segue formato `<id>@<versao>` | §2.6 |
| `invalid/missing-avaliacao.json` | Bloco `avaliacao` ausente | §3.2, §5.1 |
