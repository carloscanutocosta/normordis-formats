# Perfil de conformidade CAdES

Esta pasta define os artefactos necessários para validar o perfil criptográfico
NDF sem impor linguagem, biblioteca, fornecedor de certificados ou dispositivo.

## Fixture obrigatória para versão publicada estável

Uma fixture publicada DEVE conter:

- `payload.jcs` — bytes RFC 8785 exatos;
- `payload.sha256` — digest esperado;
- `signature.p7s` — CAdES-B-LTA detached sobre `payload.jcs`;
- `certificates/` — cadeia completa em DER;
- `revocation/` — OCSP/CRL capturados e incorporados;
- `timestamps/` — tokens RFC 3161 relevantes;
- `expected.json` — identidade, nível, algoritmos e instantes esperados;
- `trust/` — âncoras usadas exclusivamente pelo teste.

Devem existir pelo menos os seguintes casos:

| Caso | Resultado |
|---|---|
| Assinatura avançada válida | aceitar |
| Assinatura qualificada válida | aceitar como qualificada |
| Selo institucional válido | aceitar como selo, nunca como assinatura pessoal |
| Payload alterado | rejeitar |
| Contentor CAdES alterado | rejeitar |
| Timestamp alterado ou ausente | rejeitar perfil B-LTA |
| Certificado revogado antes da assinatura | rejeitar |
| Certificado expirado hoje mas válido no instante comprovado | aceitar com estado histórico explícito |
| Cadeia não confiável | rejeitar autenticidade |

Certificados de produção, chaves privadas e dados pessoais reais NÃO DEVEM ser
incluídos. Uma fixture de conformidade pode usar uma PKI de teste publicamente
documentada. A qualificação jurídica de produção exige adicionalmente um PSSC e
uma lista de confiança reais; não pode ser demonstrada por certificados de
teste.

## Gate externo

O diretório ainda não contém uma fixture B-LTA real. A especificação não DEVE
ser declarada estável até uma entidade ou laboratório competente fornecer e
validar estes artefactos com pelo menos duas stacks criptográficas distintas.

## Gerador de esqueletos

O comando de referência para preparar uma fixture esqueleto é:

```bash
python3 tools/scaffold_cades_fixture.py --all
```

Também é possível gerar um caso isolado com `--case-id`, `--case-kind` e
`--signature-kind`.

## Plano para fechar o gate

O gate só fica fechado quando existir um conjunto mínimo de fixtures
reproduzíveis, documentadas e verificadas por verificador independente.

### Conjunto mínimo de fixtures positivas

- `valid/advanced-real/` — envelope CAdES-B-LTA detached com assinatura SEA;
- `valid/qualified-real/` — envelope CAdES-B-LTA detached com assinatura SEQ;
- `valid/institutional-seal-real/` — envelope CAdES-B-LTA detached com selo institucional;
- `valid/expired-certificate-historical/` — certificado expirado no presente,
  mas válido no instante provado pelo timestamp;
- `valid/offline-tsa-real/` — timestamp RFC 3161 emitido numa TSA local ou
  isolada, com cadeia incluída no material de validação.

### Mutações negativas obrigatórias

Cada fixture positiva DEVE gerar mutações negativas explícitas:

- `negative/payload-tampered/` — `payload.jcs` alterado após a assinatura;
- `negative/signature-tampered/` — bytes do contentor CAdES alterados;
- `negative/timestamp-missing/` — remoção do timestamp B-T ou B-LTA;
- `negative/timestamp-altered/` — token RFC 3161 substituído ou corrompido;
- `negative/revocation-before-signing/` — revogação anterior ao instante
  assinado;
- `negative/chain-untrusted/` — cadeia válida mas ancorada fora do trust store;
- `negative/payload-hash-mismatch/` — digest do payload incoerente com o
  envelope.

### Critérios de aceitação

Uma fixture só entra na suite quando:

- o payload canónico corresponde exatamente a `payload.jcs`;
- `payload.sha256` é reproduzível por outra implementação;
- o conteúdo CAdES preserva o envelope original byte a byte;
- os timestamps RFC 3161 estão presentes e verificáveis;
- a cadeia de certificados e revogação está completa no material de
  validação;
- o estado histórico do certificado é explícito na fixture;
- pelo menos uma stack independente reproduz a mesma decisão;
- as mutações negativas falham pelo motivo esperado, e não por erro lateral.

### Evidência pública esperada

- hash SHA-256 de cada artefacto;
- manifesto com datas, entidade emissora e ambiente de teste;
- relatório de execução da primeira stack;
- relatório de execução da segunda stack;
- nota de limitação quando a fixture usar PKI de teste e não produção.

### Regras de segurança e privacidade

- não incluir chaves privadas de produção;
- não incluir certificados pessoais reais sem base legal e consentimento;
- não incluir dados pessoais desnecessários no payload de teste;
- se for usada PKI de teste, isso deve estar assinalado de forma explícita.
