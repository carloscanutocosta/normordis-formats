#!/usr/bin/env node
// Independent JavaScript checker for the language-neutral RFC 8785 vectors.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";

function canonicalize(value) {
  if (value === null || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new Error("non-finite number");
    return JSON.stringify(value);
  }
  if (typeof value === "string") {
    if (/[\uD800-\uDFFF]/u.test(value)) throw new Error("surrogate not permitted");
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
  return "{" + Object.keys(value).sort().map(
    key => JSON.stringify(key) + ":" + canonicalize(value[key])
  ).join(",") + "}";
}

function fromIEEE754(hex) {
  return Buffer.from(hex, "hex").readDoubleBE(0);
}

let failed = 0;
const structural = JSON.parse(readFileSync("conformance/jcs/vectors.json", "utf8"));
for (const vector of structural.vectors) {
  const bytes = Buffer.from(canonicalize(vector.value), "utf8");
  const digest = createHash("sha256").update(bytes).digest("hex");
  const ok = bytes.toString("hex") === vector.canonical_utf8_hex && digest === vector.sha256;
  console.log(ok ? "PASS" : "FAIL", vector.id);
  failed += ok ? 0 : 1;
}

const numbers = JSON.parse(readFileSync("conformance/jcs/numbers.json", "utf8"));
for (const [hex, expected] of numbers.vectors) {
  const ok = canonicalize(fromIEEE754(hex)) === expected;
  console.log(ok ? "PASS" : "FAIL", "number-" + hex);
  failed += ok ? 0 : 1;
}
for (const hex of numbers.must_reject) {
  let ok = false;
  try { canonicalize(fromIEEE754(hex)); } catch { ok = true; }
  console.log(ok ? "PASS" : "FAIL", "reject-" + hex);
  failed += ok ? 0 : 1;
}

process.exitCode = failed ? 1 : 0;
