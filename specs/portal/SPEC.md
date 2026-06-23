# Portal público de verificação NORMORDIS

**Versão:** 1.0.0
**Estado:** Draft — Revisão pública

## 1. Objetivo e âmbito

O portal é um serviço de custódia que resolve um `validation_code`. O código
não constitui uma assinatura e o portal não expõe o conteúdo NDF. O contrato
machine-readable independente da língua encontra-se em `openapi.yaml`.

## 2. Procedimento de verificação

Para cada consulta bem-sucedida, o serviço DEVE:

1. resolver o registo exato sem depender de metadados fornecidos pelo
   utilizador;
2. recalcular JCS e `payload_hash` a partir do NDF-core preservado;
3. recalcular e comparar `validation_code`;
4. validar a cadeia de custódia e a última âncora externa;
5. validar CAdES, timestamps, revogação e confiança, quando presentes;
6. obter o estado arquivístico corrente;
7. devolver separadamente os estados de integridade, autenticidade e
   assinatura.

`trusted_custody` significa que o portal atesta emissão e preservação pela
instituição identificada. NÃO DEVE ser apresentado como assinatura eletrónica
pessoal. `integrity_only` NÃO DEVE ser apresentado como prova da identidade do
emissor.

## 3. Privacidade e resistência a abuso

A resposta pública DEVE conter apenas entidade produtora, tipo, data de
finalização e estado. Assunto, destinatário, identificadores pessoais,
classificação, conteúdo e detalhes de conservação NÃO DEVEM ser expostos.

O serviço DEVE limitar enumeração, registar abuso e devolver a mesma resposta
para registos desconhecidos e não públicos. Os logs DEVEM ter prazo de
conservação documentado. Respostas cujo estado possa mudar NÃO DEVEM usar cache
pública incompatível com essa mudança.

## 4. Disponibilidade e verificação offline

Indisponibilidade do portal produz `unavailable`, nunca `invalid`. Pacotes
assinados ou selados permanecem verificáveis offline. Autenticidade baseada
apenas em custódia exige réplica confiável ou âncora exportada verificável.

## 5. Confiança operacional

O operador DEVE publicar identidade, contacto de segurança, política de
incidentes, versões suportadas, atualização de listas de confiança e histórico
de auditoria. RECOMENDA-SE assinar respostas ou publicar um log de
transparência que permita provar uma resposta sem depender de captura de ecrã.
