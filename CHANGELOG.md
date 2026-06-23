# Histórico de alterações

As alterações relevantes às especificações NORMORDIS são registadas aqui. Cada
formato mantém também o seu histórico em `specs/<formato>/CHANGELOG.md`.

## [Não publicado]

### Harmonização editorial e de normalização

- estado comum `Draft — Revisão pública` para NDF, NDT e NCRTF;
- política editorial, língua normativa e estrutura documental comum;
- regras de consenso, votação, recurso, conflitos de interesse e IPR;
- referências normativas controladas e migração de RFC 4122 para RFC 9562;
- alegações jurídicas reformuladas como objetivos técnicos condicionados;
- terminologia e ortografia portuguesa harmonizadas;
- matriz de rastreabilidade expandida com prefixos estáveis de requisitos.
- auditoria automática de 45 IDs e inventário de declarações subordinadas;
- sete vetores negativos de pacote `.ndfpkg`;
- corpus semântico NDT com nove casos estáveis;
- dossier de revisão pública autocontido e verificado por hashes;
- gates editoriais e normativos integrados na CI.

## [2026-06-20] — NDT v2.0.0 e harmonização NDF/NCRTF

### NDT

- formato declarativo de layout sem motor de regras de negócio;
- `versao_ndt` substitui `versao_impresso`;
- layout de fluxo, campo de assinatura e estilos globais;
- mapeamento NCRTF ↔ NDT;
- suporte estrutural a PDF/UA-2 e PDF/A-3;
- exemplos e suite de conformidade NDT.

### NDF / NCRTF

- harmonização do mapeamento tipográfico;
- revisão de consistência entre schemas e exemplos.

## [2026-06-18] — NCRTF v2.0.0 e NDF v1.0.0

### NCRTF

- listas unificadas, tabelas simplificadas e `font_family` explícito;
- nós `link`, `hard_break` e `blockquote`;
- novas marcas e regras de canonicalização.

### NDF

- estrutura NDF-core, envelope, avaliação arquivística, finalização,
  proveniência e versionamento.

### Repositório

- suites de conformidade NDF e NCRTF;
- schemas JSON para NDF, NDT, NCRTF, envelope, manifesto e registo;
- validador de referência;
- ADR sobre a escolha de JSON.
