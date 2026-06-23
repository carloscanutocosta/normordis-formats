# Exemplo `.ndfpkg`

Este diretório representa o conteúdo interno de um ficheiro `documento.ndfpkg`.

Um `.ndfpkg` é um arquivo ZIP com esta estrutura exata. Para criar o pacote:

```bash
cd ndfpkg-example/
zip -r ../documento.ndfpkg manifest.json ndf-core.json envelope.json ndt/ schemas/ recursos/
```

## Ficheiros

| Ficheiro | Descrição |
|---|---|
| `manifest.json` | Inventário do pacote com hashes de integridade |
| `ndf-core.json` | Bytes canónicos do NDF-core (JCS/RFC 8785, UTF-8) |
| `envelope.json` | Assinaturas, timestamps, validation_code, estado operacional |
| `ndt/oficio-generico@2.0.0.ndt.json` | NDT referenciado por `ndt_version_ref` |
| `schemas/` | Schemas NDF, envelope, manifest, custódia, NDT, NCRTF e tipo `oficio` usados pelo pacote |

**Nota**: os valores de `cades_b_lta`, `assinatura` (timestamps) e `cadeia_certificados` neste exemplo são placeholders não funcionais. Um `.ndfpkg` real conteria os bytes DER/Base64 correctos da assinatura CAdES-B-LTA e dos timestamps RFC 3161.
