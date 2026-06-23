# Plano de revisão pública

## Objeto

Revisão coordenada de NDF 1.0.0, NDT 2.0.0 e NCRTF 2.0.0 enquanto drafts,
incluindo schemas, exemplos e suites de conformidade.

## Preparação

- [ ] fixar commit e hashes dos artefactos;
- [ ] publicar índice de requisitos e matriz de rastreabilidade;
- [ ] indicar questões editoriais e técnicas em aberto;
- [ ] convidar representantes de arquivo, Administração Pública, indústria,
  academia, acessibilidade, segurança, proteção de dados e utilizadores;
- [ ] anunciar prazo mínimo de 45 dias;
- [ ] nomear editores e responsáveis pela decisão;
- [ ] publicar política de conflitos de interesse e IPR.

O dossier técnico é gerado por:

```bash
python3 tools/build_review_bundle.py
```

Em árvore de trabalho não limpa, `--allow-dirty` produz apenas uma
pré-visualização marcada como tal e não deve ser publicada.

## Tratamento de comentários

Cada comentário é registado em `REVIEW-LOG.md`, recebe resposta fundamentada e
é ligado ao commit que o resolve. Objeções não resolvidas são apresentadas com
a posição minoritária. Alterações normativas reiniciam a revisão quando
afetarem substancialmente o âmbito ou a interoperabilidade.

## Saídas

- relatório de comentários e decisões;
- lista de participantes por categoria de stakeholder;
- nova matriz de rastreabilidade;
- resultados das implementações independentes;
- recomendação fundamentada de manter Draft ou promover a Candidata.
