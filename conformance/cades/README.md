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
