# Gates de normalização NORMORDIS

Um formato pode ser tecnicamente normalizável antes de estar pronto para
submissão ou publicação. Este documento impede que maturidade arquitectural
seja confundida com evidência de interoperabilidade.

## Gates internos

| Gate | Critério | Estado |
|---|---|---|
| Arquitetura comum | responsabilidades NDF/NDT/NCRTF coerentes | revista; manter auditoria cruzada |
| Schemas | todos válidos e versionados exactamente | concluído |
| Pacote | exemplo autocontido com inventário e hashes verificáveis | concluído |
| JCS | ferramenta + vetores independentes de linguagem, incluindo RFC 8785 Appendix B | concluído e cruzado em Python/JavaScript; outras stacks desejáveis |
| Custódia | schema, cadeia de hashes, âncora e casos negativos | cadeia verificada; integração WORM/TSA externa pendente |
| Portal | OpenAPI e semântica de autenticidade/privacidade | contrato concluído; implementação e revisão de segurança pendentes |
| NDT | corpus semântico com 9 casos; extravasamento, recursos e acessibilidade | cobertura estrutural concluída; resultados extraídos de renderizadores independentes pendentes |
| CAdES | fixtures B-LTA reais positivas e negativas | plano operativo em `CADES-GATE-PLAN.md`; verificador em `tools/check_cades_gate.py`; evidência externa ainda pendente |
| Eficiência | corpus e medições reproduzíveis | metodologia e medição inicial concluídas; corpus institucional pendente |
| Pacote | exemplo positivo e vetores negativos de inventário, caminhos, NDT e envelope | 1 positivo + 7 negativos concluídos |
| Auditoria editorial | modalidade, IDs, estrutura de publicação e dossier com hashes | automatizada em CI |

## Gates externos

Antes de declarar qualquer especificação estável:

1. execução do plano de fixtures CAdES em `CADES-GATE-PLAN.md`;
2. revisão criptográfica independente do perfil CAdES e renovação;
3. revisão arquivística por especialista competente;
4. revisão jurídica portuguesa/eIDAS, sem alegações de equivalência não
   suportadas;
5. revisão de acessibilidade dos perfis de saída;
6. implementação ou piloto independente que passe a suite sem consultar código
   interno do produtor original;
7. manifestação documentada de necessidade por utilizadores institucionais;
8. definição da Comissão Técnica, âmbito e estratégia NP/CEN/ISO.

Nenhum maintainer pode marcar estes gates como concluídos apenas com revisão
interna. Relatórios, versões das ferramentas, resultados e conflitos de
interesse devem ser públicos.
