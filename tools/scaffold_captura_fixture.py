#!/usr/bin/env python3
"""Gera o PDF mínimo usado como componente 'original' do exemplo de captura.

Determinístico e sem dependências: os mesmos bytes em qualquer máquina, para
que o digest declarado no NDF-core seja reproduzível por terceiros. Não é um
PDF/A conforme — é deliberadamente um PDF simples, para que o exemplo exercite
o caso 'nao_conforme' de validacao_formato (SPEC §2.4 do plano de captura).
"""

from pathlib import Path

DESTINO = (Path(__file__).resolve().parent.parent
           / "specs/ndf/examples/captura-requerimento/original/requerimento.pdf")

TEXTO = "Requerimento de certidao de teor - exemplo NORMORDIS"


def build() -> bytes:
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        None,  # fluxo de conteudo, preenchido abaixo
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    fluxo = f"BT /F1 12 Tf 60 760 Td ({TEXTO}) Tj ET".encode("ascii")
    objetos[3] = b"<< /Length " + str(len(fluxo)).encode() + b" >>\nstream\n" + fluxo + b"\nendstream"

    saida = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, corpo in enumerate(objetos, start=1):
        offsets.append(len(saida))
        saida += f"{i} 0 obj\n".encode() + corpo + b"\nendobj\n"

    inicio_xref = len(saida)
    saida += f"xref\n0 {len(objetos) + 1}\n".encode()
    saida += b"0000000000 65535 f \n"
    for off in offsets:
        saida += f"{off:010d} 00000 n \n".encode()
    saida += (
        f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\n"
        f"startxref\n{inicio_xref}\n%%EOF\n"
    ).encode()
    return bytes(saida)


if __name__ == "__main__":
    dados = build()
    DESTINO.write_bytes(dados)
    import hashlib
    print(f"{DESTINO.name}: {len(dados)} bytes, sha256:{hashlib.sha256(dados).hexdigest()}")
