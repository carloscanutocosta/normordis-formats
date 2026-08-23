# Exemplo `.ndfpkg`

Este diretório representa o conteúdo interno de um ficheiro `documento.ndfpkg`.

Um `.ndfpkg` é um arquivo ZIP com esta estrutura exata. Para criar o pacote:

```bash
cd ndfpkg-example/
zip -r ../documento.ndfpkg manifest.json ndf-core.json envelope.json ndt/ schemas/ recursos/ anexos/
```

## Ficheiros

| Ficheiro | Descrição |
|---|---|
| `manifest.json` | Inventário do pacote com hashes de integridade |
| `ndf-core.json` | Bytes canónicos do NDF-core (JCS/RFC 8785, UTF-8) |
| `envelope.json` | Assinaturas, timestamps, validation_code, estado operacional |
| `ndt/oficio-generico@2.0.0.ndt.json` | NDT referenciado por `ndt_version_ref` |
| `schemas/` | Schemas NDF, envelope, manifest, custódia, NDT, NCRTF e tipo `oficio` usados pelo pacote |
| `anexos/mapa-medicoes.txt` | Anexo do ofício, declarado em `documento.componentes[]` com `papel: "anexo"` |

**Nota**: os valores de `cades_b_lta`, `assinatura` (timestamps) e `cadeia_certificados` neste exemplo são placeholders não funcionais. Um `.ndfpkg` real conteria os bytes DER/Base64 correctos da assinatura CAdES-B-LTA e dos timestamps RFC 3161.

## Um documento nativo com anexo

Este ofício exercita §2.8.1.3: o ato vive nos campos estruturados de
`oficio@1.0.0` e o anexo é um componente binário do mesmo NDF.

```json
"componentes": [
  {
    "id": "mapa-medicoes",
    "papel": "anexo",
    "media_type": "text/plain",
    "sha256": "sha256:165830ce…",
    "tamanho": 130,
    "nome_original": "mapa-medicoes.txt"
  }
]
```

O digest está nos `payload_bytes`, logo coberto pela assinatura: alterar o anexo
obriga a alterar o NDF-core e quebra a assinatura do documento. O ficheiro viaja
em `anexos/`, e `NDF-PKG-009` fecha nos dois sentidos — um pacote a que falte o
anexo declarado, ou que leve em `anexos/` um ficheiro não declarado, não é
conforme (`PKG-NEG-015`, `PKG-NEG-016`).

Se o anexo tivesse identidade documental própria — autor, data, número, avaliação
ou ciclo de vida próprios — seria NDF autónomo, ligado por
`relacoes[{ tipo: "anexa" }]`, e não um componente. Ver ADR-025.
