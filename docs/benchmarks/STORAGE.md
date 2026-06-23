# Eficiência de armazenamento

O objetivo NDF é minimizar redundância sem sacrificar interpretação,
integridade ou portabilidade. Não existe um limite universal em bytes: CAdES,
certificados, NCRTF e recursos variam por documento.

## Metodologia

Cada benchmark DEVE publicar, para o mesmo corpus:

1. bytes de `ndf-core.json` em JCS;
2. bytes do envelope sem e com CAdES-B-LTA;
3. bytes dos schemas, NDT e recursos;
4. tamanho do `.ndfpkg` ZIP;
5. tamanho físico do perfil de custódia com deduplicação;
6. tamanho do PDF/ODF comparável, quando existir;
7. tempo e memória de validação, canonicalização, embalagem e leitura.

Resultados DEVEM separar conteúdo único de objetos deduplicáveis. Não é válido
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

---

## Medições iniciais — corpus de referência

**Ambiente:** Linux WSL2 · Python 3 · gzip -9  
**Fixture:** `specs/ndf/examples/ndfpkg-example` (ofício com NCRTF, assinatura qualificada)  
**Comando:** `python3 tools/measure.py specs/ndf/examples/ndfpkg-example`  
**Estado:** estimativa de desenvolvimento — envelope com CAdES-B-LTA real pendente (gate externo)

### Perfil portátil `.ndfpkg` — breakdown completo

| Ficheiro | Bytes | Bytes gz |
|---|---:|---:|
| `ndf-core.json` | 3 377 | 1 320 |
| `envelope.json` (placeholder) | 1 304 | 651 |
| `ndt/oficio-generico@2.0.0.ndt.json` | 7 240 | 1 409 |
| `recursos/brasao-republica.svg` | 904 | 529 |
| `schemas/ndf-core.schema.json` | 8 906 | 2 663 |
| `schemas/envelope.schema.json` | 5 760 | 1 816 |
| `schemas/ndt.schema.json` | 27 499 | 3 147 |
| `schemas/ncrtf.schema.json` | 6 554 | 1 170 |
| `schemas/oficio.schema.json` | 4 097 | 1 280 |
| `schemas/manifest.schema.json` | 1 633 | 648 |
| `schemas/custody-event.schema.json` | 1 649 | 609 |
| **Total portátil** | **68 923** | **15 242** |

O pacote portátil comprime para **14,9 KB gz** — inclui schemas completos e NDT,
que numa BD são deduplicados e não se repetem por documento.

### Perfil de custódia — custo marginal por documento em BD

O perfil de custódia armazena apenas `ndf-core` e `envelope`; NDTs, schemas,
certificados e recursos são deduplicados por hash dentro do domínio de custódia.

#### Envelope com assinatura qualificada real (estimativa CAdES-B-LTA)

O envelope de placeholder ocupa 1,3 KB. Um envelope com assinatura qualificada
real inclui material criptográfico que domina o tamanho:

| Componente | Estimativa |
|---|---:|
| Certificado do signatário (DER → base64) | ~2 800 B |
| Certificado CA intermédia (DER → base64) | ~2 100 B |
| Certificado CA raiz (DER → base64) | ~1 600 B |
| OCSP response capturada (DER → base64) | ~2 200 B |
| Timestamp B-T / RFC 3161 (base64) | ~3 200 B |
| Timestamp B-LTA / RFC 3161 (base64) | ~4 100 B |
| CMS SignedData wrapper + overhead | ~800 B |
| **Total envelope qualificado estimado** | **~16 800 B (~16,4 KB)** |

Estes valores são estimativas baseadas em observação de serviços eIDAS portugueses;
variam com a CA, o comprimento da cadeia e a resposta OCSP. A medição real requer
fixtures CAdES-B-LTA produzidas externamente (gate ainda pendente em READINESS.md).

#### Custo por documento — perfil de custódia

| Tipo de documento | ndf-core | envelope | **Total BD** | gz |
|---|---:|---:|---:|---:|
| Ofício curto, sem assinatura (integridade apenas) | ~3 KB | ~1 KB | **~5 KB** | ~2 KB |
| Ofício, assinatura qualificada CAdES-B-LTA | ~3 KB | ~17 KB | **~21 KB** | ~12 KB |
| Ofício longo (corpo NCRTF extenso) | ~12 KB | ~17 KB | **~30 KB** | ~16 KB |
| Modelo 3 IRS — Rosto + Anexo A (1 empregador) | ~22 KB | ~17 KB | **~40 KB** | ~19 KB |
| Modelo 3 IRS — declaração complexa (5+ anexos) | ~78 KB | ~17 KB | **~96 KB** | ~41 KB |

O envelope domina o custo de documentos curtos. Em documentos longos (Modelo 3
complexo), o ndf-core torna-se o factor dominante, mas permanece estruturado e
pesquisável — ao contrário de um PDF.

#### Custo amortizado — objetos deduplicáveis (custo único por versão)

| Objecto | Tamanho |
|---|---:|
| Schemas completos (todos os tipos) | ~62 KB |
| NDT `oficio-generico@2.0.0` | ~7 KB |
| NDT Modelo 3 (Rosto + Anexo A + Anexo G) | ~12 KB |
| Logo/brasão da entidade (SVG, partilhado) | ~1 KB |

A partir do **segundo documento** do mesmo tipo e versão, o custo marginal em BD
é apenas `ndf-core + envelope`. Para uma entidade com 10 000 ofícios por ano,
os 62 KB de schemas pagam-se uma vez.

### Comparação com formatos alternativos

Mesmo ofício assinado, armazenado em BD (estimativas):

| Formato | Tamanho em BD |
|---|---:|
| NDF ndf-core + envelope (sem assinatura) | **~5 KB** |
| **NDF ndf-core + envelope (assinatura qualificada)** | **~21 KB** |
| DOCX equivalente | ~44 KB |
| PDF/A sem assinatura | ~54 KB |
| PDF/A com PAdES-B-LTA | ~78 KB |

O NDF não armazena layout nem renderização — estes são responsabilidade do NDT,
deduplicado, e do renderizador, substituível. A separação entre dados (NDF-core) e
apresentação (NDT) é a principal fonte de eficiência em arquivo.

Numa projeção não vinculativa para 1 milhão de ofícios assinados:

| Formato | Estimativa total |
|---|---:|
| NDF (assinatura qualificada) | **~21 GB** |
| PDF/A + PAdES-B-LTA | ~78 GB |

Esta projeção assume documentos homogéneos e envelope de tamanho fixo; na
prática o ndf-core varia com o conteúdo. **Não deve ser usada como garantia
contratual** até existirem medições sobre corpus institucional real.

### Próximos passos de benchmarking

- [ ] Medição com envelope CAdES-B-LTA real (aguarda gate externo)
- [ ] Corpus de informação técnica longa com tabelas e imagens
- [ ] Corpus Modelo 3 IRS com dados reais anonimizados
- [ ] Medição de tempo de validação, canonicalização e embalagem
- [ ] Comparação com sistemas de arquivo documentais existentes (ECM/EDMS)
