# Política de segurança

## Comunicação responsável

Não abra uma issue pública para comunicar uma vulnerabilidade, uma exposição de
dados, uma chave acidentalmente publicada ou um problema que permita adulterar
artefactos de conformidade.

Em vez disso, use a opção **Report a vulnerability** no separador **Security**
do repositório GitHub e inclua:

- uma descrição clara do impacto;
- passos mínimos para reproduzir, ou uma prova de conceito não destrutiva;
- a versão, ficheiros ou hashes afetados; e
- uma forma segura de contacto para acompanhamento.

Se essa opção não estiver disponível, o maintainer deve ativar *private
vulnerability reporting* nas definições de segurança do repositório antes da
publicação.

## Âmbito

São especialmente relevantes vulnerabilidades nas ferramentas de validação,
nos schemas, nos vetores criptográficos e na integridade dos pacotes `.ndfpkg`.
Este repositório não é um serviço alojado e não recebe documentos reais nem
segredos operacionais.

## Tratamento

O maintainer confirma a receção, avalia a reprodução e coordena a divulgação.
Não publique detalhes antes de existir uma correção, mitigação ou decisão
documentada. Problemas que afetem uma versão publicada são registados no
changelog e, quando aplicável, recebem um identificador de advisory GitHub.

Se a vulnerabilidade estiver a ser **ativamente explorada**, ou constituir um
incidente grave de segurança, aplica-se adicionalmente o procedimento de
notificação regulatória em [`CRA_REPORTING.md`](CRA_REPORTING.md) (Cyber
Resilience Act, Artigo 14), com prazos de 24h/72h/14 dias para o CSIRT
nacional e a ENISA.

## Regras para contribuidores

Nunca inclua tokens, palavras-passe, chaves privadas, certificados privados,
dados pessoais reais ou documentos operacionais. Exemplos e fixtures devem usar
dados sintéticos ou publicamente verificáveis.
