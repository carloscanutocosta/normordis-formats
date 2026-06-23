# Perfil editorial para publicação normativa

## Finalidade

Este perfil define a transformação da edição de trabalho do repositório numa
proposta para IPQ, CEN ou ISO. Não atribui estatuto oficial ao documento.

## Ordem da proposta

Cada formato é preparado com a seguinte ordem:

1. preâmbulo editorial;
2. objetivo e âmbito;
3. referências normativas;
4. termos, definições, símbolos e abreviaturas;
5. arquitetura e requisitos técnicos;
6. perfis e declaração de conformidade;
7. anexos normativos;
8. anexos informativos;
9. bibliografia.

Histórico, roadmap, benchmarks, orientações jurídicas, exemplos extensos e
perfis físicos de base de dados não são intercalados nas cláusulas normativas.

## Regras de transformação

- A numeração da proposta é regenerada; referências cruzadas são verificadas
  automaticamente antes de publicação.
- Cada requisito mantém o identificador estável do repositório mesmo que o
  número da cláusula mude.
- Exemplos e notas são marcados como informativos.
- Schemas, vetores e algoritmos normativos são anexados ou referenciados por
  versão e hash.
- A versão submetida inclui índice de requisitos e matriz de comentários.
- O template e metadados finais são os do organismo destinatário.

## Mapa corrente

| Formato | Corpo normativo | Material informativo separado | Lacuna editorial principal |
|---|---|---|---|
| NDF | `specs/ndf/SPEC.md` | `NDF-INFORMATIVE-GUIDANCE.md`, benchmarks e roadmap | converter glossário em termos formais e fechar referências cruzadas |
| NDT | `specs/ndt/SPEC.md` | `specs/ndt/ROADMAP.md` | mover termos para a abertura e separar perfis de saída informativos |
| NCRTF | `specs/ncrtf/SPEC.md` | changelog e exemplos | mover termos para a abertura e classificar exemplos |

## Critério de conclusão

Uma proposta só é gerada quando o auditor normativo não encontra requisitos sem
identificador, referências quebradas, modalidades ambíguas ou material
informativo não classificado.
