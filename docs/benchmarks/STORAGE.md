# Metodologia de eficiência de armazenamento

O objectivo NDF é minimizar redundância sem sacrificar interpretação,
integridade ou portabilidade. Não existe um limite universal em bytes: CAdES,
certificados, NCRTF e recursos variam por documento.

## Métricas obrigatórias

Cada benchmark DEVE publicar, para o mesmo corpus:

1. bytes de `ndf-core.json` em JCS;
2. bytes do envelope sem e com CAdES-B-LTA;
3. bytes dos schemas, NDT e recursos;
4. tamanho do `.ndfpkg` ZIP;
5. tamanho físico do perfil de custódia com deduplicação;
6. tamanho do PDF/ODF comparável, quando existir;
7. tempo e memória de validação, canonicalização, embalagem e leitura.

Resultados DEVEM separar conteúdo único de objectos deduplicáveis. Não é válido
afirmar uma percentagem geral de poupança a partir de um único documento.

## Corpus mínimo

- ofício curto sem assinatura;
- ofício com NCRTF e assinatura qualificada;
- informação técnica longa com tabelas e imagens;
- formulário fiscal com milhares de campos;
- documento com múltiplos anexos e recursos repetidos.

O corpus, comandos, versões, sistema operativo e resultados brutos devem ser
publicados. Medições são informativas; nunca alteram os requisitos de
integridade ou autocontenção do perfil portátil.

Use `python3 tools/measure.py <ficheiros/directórios>` para obter medidas
reproduzíveis de bytes e compressão. A ferramenta é apenas uma conveniência;
qualquer linguagem pode calcular as mesmas métricas.
