# Plano para fechar o gate CAdES B-LTA

## Objetivo

Subir o perfil criptográfico do projeto de “gate externo pendente” para
“evidência independente suficiente”, sem misturar fixtures de teste com
material de produção.

## Resultado esperado

O gate fica fechado quando houver:

1. pelo menos uma fixture positiva SEA;
2. pelo menos uma fixture positiva SEQ;
3. pelo menos uma fixture positiva de selo institucional;
4. mutações negativas derivadas de cada fixture positiva;
5. reprodução da mesma decisão em duas stacks independentes;
6. documentação pública da origem, ambiente e limitações.

## Pacote mínimo de artefactos

Cada caso deve publicar os seguintes itens:

- `payload.jcs`
- `payload.sha256`
- `signature.p7s`
- `certificates/`
- `revocation/`
- `timestamps/`
- `expected.json`
- `trust/`
- `manifest.json`

Os modelos de manifesto estão em `conformance/cades/manifests/` e os modelos
de expectativa estão em `conformance/cades/expected/`.

## Checklist executável

### Fase 1 — Preparação do corpus

- fixar a origem da PKI de teste ou da entidade emissora real;
- registar a data, hora e ambiente de geração;
- gerar `payload.jcs` por canonicalização JCS;
- calcular e publicar `payload.sha256`;
- criar `manifest.json` com hashes e metadados de origem;
- guardar a âncora de confiança em `trust/`.

### Fase 2 — Geração das fixtures positivas

- produzir a fixture SEA válida;
- produzir a fixture SEQ válida;
- produzir a fixture de selo institucional válida;
- produzir a fixture com certificado expirado, mas validável historicamente;
- produzir a fixture com TSA local ou isolada;
- verificar que cada caso preserva `signature.p7s`, `timestamps/` e
  `revocation/` completos.

### Fase 3 — Derivação das negativas

- alterar `payload.jcs` e confirmar rejeição;
- alterar `signature.p7s` e confirmar rejeição;
- remover o timestamp B-T e confirmar rejeição;
- remover o timestamp B-LTA e confirmar rejeição;
- corromper um token RFC 3161 e confirmar rejeição;
- introduzir revogação anterior ao instante assinado e confirmar rejeição;
- mover a âncora de confiança para fora do trust store e confirmar rejeição.

### Fase 4 — Verificação independente

- executar a primeira stack de validação;
- executar uma segunda stack independente;
- comparar a decisão e o motivo da decisão;
- registar divergências e corrigir a fixture se necessário.

### Fase 5 — Publicação

- publicar os hashes finais;
- publicar o relatório de validação;
- publicar a nota de limitação se a PKI for de teste;
- marcar o gate como fechado apenas quando as duas stacks coincidirem.

## Casos positivos

### 1. Assinatura avançada válida

- Envelope com CAdES-B-LTA detached;
- certificado SEA;
- timestamp B-T;
- timestamp B-LTA;
- material de validação completo.

### 2. Assinatura qualificada válida

- Envelope com CAdES-B-LTA detached;
- certificado SEQ;
- timestamp B-T;
- timestamp B-LTA;
- estado histórico de confiança explícito.

### 3. Selo institucional válido

- Envelope com CAdES-B-LTA detached;
- certificado institucional;
- o verificador aceita como integridade institucional;
- o verificador não alega assinatura pessoal.

### 4. Certificado expirado, mas historicamente válido

- O certificado já está expirado no presente;
- o instante da assinatura e a cadeia permitem validação histórica;
- o resultado deve declarar o estado histórico.

### 5. TSA local ou isolada

- timestamp RFC 3161 emitido fora de internet pública;
- cadeia de confiança completa no material de validação;
- trust store da fixture assinala a âncora usada.

## Casos negativos

De cada caso positivo devem ser geradas, pelo menos, as seguintes mutações:

- payload alterado;
- assinatura alterada;
- timestamp ausente;
- timestamp corrompido;
- cadeia revogada antes da assinatura;
- cadeia ancorada fora do trust store;
- digest do payload incoerente.

## Critérios de aceitação

Uma fixture só é aceite se:

- tiver hash e manifesto publicados;
- for reproduzível fora do produtor original;
- passar numa stack independente;
- falhar nas mutações negativas pelo motivo correto;
- não depender de segredos de produção;
- declarar claramente se usa PKI de teste.

## Resultado verificável

O gate pode ser dado como fechado quando todos estes pontos forem verdade:

- existem pelo menos três fixtures positivas publicadas;
- cada fixture positiva tem pelo menos uma mutação negativa associada;
- uma segunda stack reproduz as mesmas decisões;
- o relatório indica claramente o instante de verificação e o ambiente;
- o diretório não contém placeholders funcionais disfarçados de prova real.

O verificador de referência é `tools/check_cades_gate.py`.

## Nota de interpretação

Este plano melhora a robustez do perfil CAdES, mas não substitui revisão
jurídica, arquivística ou de acreditação. Essas validações continuam a ser
gates externos.
