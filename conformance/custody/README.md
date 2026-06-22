# Custody-chain conformance

The JSON files are language-neutral fixtures. `valid-chain.json` must be
accepted and `invalid-chain.json` rejected. Event hashes cover the RFC 8785
bytes of each event after removing only `event_hash`.

Reference commands:

```bash
node tools/check-custody.mjs conformance/custody/valid-chain.json
! node tools/check-custody.mjs conformance/custody/invalid-chain.json
```
