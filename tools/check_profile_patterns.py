#!/usr/bin/env python3
"""Verifica coerência entre `pattern` e `examples` nos schemas de perfil.

Nasceu do achado R19 (avaliação externa, 2026-09-11): o schema `pt-dglab`
declarava `ts/at/300.20` como exemplo de `classificacao_ref`, mas a própria
regex do campo rejeitava esse valor — um `PASS` verde nunca teria apanhado
isto, porque nenhuma suite testava os exemplos contra o seu próprio schema.

Duas verificações, para a mesma classe de defeito não voltar a passar
despercebida:

1. Positiva: cada `examples[]` declarado tem de validar contra o `pattern`
   do mesmo campo.
2. Negativa: um pequeno conjunto de valores intencionalmente inválidos
   (espaços, segmentos vazios) tem de continuar rejeitado. Não é
   exaustivo — é a memória dos casos que já escaparam uma vez.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = ROOT / "specs/registry/profiles"

# Casos que já escaparam à regex antiga do pt-dglab (revisão externa,
# 2026-09-11): espaço, segmento vazio a meio, segmento vazio no fim.
NEGATIVE_CASES = {
    "pt-dglab.schema.json": {
        "classificacao_ref": ["ts/", "ts/ ", "ts//", "ts/at/", "ts /at/300.20"],
        "instrumento_ref": ["ts/", "ts/ ", "ts//", "ts/at/"],
    },
}


def main() -> int:
    failures = []
    checked_examples = 0
    checked_negatives = 0

    for schema_path in sorted(PROFILE_DIR.glob("*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        properties = schema.get("properties", {})
        for field, definition in properties.items():
            if not isinstance(definition, dict):
                continue
            pattern = definition.get("pattern")
            examples = definition.get("examples")
            if pattern and examples:
                compiled = re.compile(pattern)
                for example in examples:
                    checked_examples += 1
                    if not compiled.fullmatch(example) and not compiled.match(example):
                        failures.append(
                            f"{schema_path.name}: {field}.examples contém "
                            f"'{example}', que não passa no próprio pattern "
                            f"'{pattern}'"
                        )
            negatives = NEGATIVE_CASES.get(schema_path.name, {}).get(field)
            if pattern and negatives:
                compiled = re.compile(pattern)
                for bad in negatives:
                    checked_negatives += 1
                    if compiled.match(bad):
                        failures.append(
                            f"{schema_path.name}: {field}.pattern aceita "
                            f"'{bad}', que deveria ser rejeitado"
                        )

    if failures:
        for f in failures:
            print(f"FAIL {f}")
        print(f"FAIL profile patterns: {len(failures)} problemas")
        return 1

    print(
        f"PASS profile patterns: {checked_examples} exemplos, "
        f"{checked_negatives} casos negativos"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
