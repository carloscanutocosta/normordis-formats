# Corpus semântico NDT

O corpus fixa entradas e expectativas independentes do motor. Nesta fase valida
cobertura estrutural, identidade e presença das primitivas. Um renderizador
independente deverá acrescentar árvores semânticas extraídas e resultados de
referência sem alterar os IDs `NDT-SEM-*`.

```bash
python3 tools/check_ndt_semantic_corpus.py
```

As entradas `future_semantic_assertions` são gates declarados, não resultados
já demonstrados. Não devem ser apresentadas como cobertura concluída.
