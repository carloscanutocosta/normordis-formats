# RFC 8785 / JCS conformance

`vectors.json` is the language-neutral structural contract: implementations compare the
exact UTF-8 bytes and SHA-256 digest, not textual JSON formatting. Additional
IEEE-754 serialization cases from RFC 8785 Appendix B are in `numbers.json`.

The Python convenience check is:

```bash
python3 tools/check_jcs_vectors.py
```

An independent JavaScript check is also provided:

```bash
node tools/check-jcs-vectors.mjs
```

C#, Rust, Go, Java and other implementations consume the same JSON vectors and
must produce identical bytes.
