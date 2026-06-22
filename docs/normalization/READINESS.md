# Gates de normalização NORMORDIS

Um formato pode ser tecnicamente normalizável antes de estar pronto para
submissão ou publicação. Este documento impede que maturidade arquitectural
seja confundida com evidência de interoperabilidade.

## Gates internos

| Gate | Critério | Estado |
|---|---|---|
| Arquitectura comum | responsabilidades NDF/NDT/NCRTF sem contradição | concluído |
| Schemas | todos válidos e versionados exactamente | concluído |
| Pacote | exemplo autocontido com inventário e hashes verificáveis | concluído |
| JCS | ferramenta + vectores independentes de linguagem, incluindo RFC 8785 Appendix B | concluído e cruzado em Python/JavaScript; outras stacks desejáveis |
| Custódia | schema, cadeia de hashes, âncora e casos negativos | cadeia concluída; integração WORM/TSA externa pendente |
| Portal | OpenAPI e semântica de autenticidade/privacidade | contrato concluído; implementação e revisão de segurança pendentes |
| NDT | semântica, overflow, recursos, acessibilidade e golden outputs | parcial |
| CAdES | fixtures B-LTA reais positivas e negativas | pendente externo |
| Eficiência | corpus e medições reproduzíveis | metodologia e medição inicial concluídas; corpus institucional pendente |

## Gates externos

Antes de declarar o conjunto estável:

1. revisão criptográfica independente do perfil CAdES e renovação;
2. revisão arquivística por especialista competente;
3. revisão jurídica portuguesa/eIDAS, sem alegações de equivalência não
   suportadas;
4. revisão de acessibilidade dos perfis de saída;
5. implementação ou piloto independente que passe a suite sem consultar código
   interno do produtor original;
6. manifestação documentada de necessidade por utilizadores institucionais;
7. definição da Comissão Técnica, âmbito e estratégia NP/CEN/ISO.

Nenhum maintainer pode marcar estes gates como concluídos apenas com revisão
interna. Relatórios, versões das ferramentas, resultados e conflitos de
interesse devem ser públicos.
