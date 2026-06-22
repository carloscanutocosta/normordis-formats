#!/usr/bin/env node
// Reference checker for the language-neutral NDF custody-chain vectors.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";

function canonicalize(value) {
  if (value === null || typeof value === "boolean" || typeof value === "number" || typeof value === "string") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
  return "{" + Object.keys(value).sort().map(
    key => JSON.stringify(key) + ":" + canonicalize(value[key])
  ).join(",") + "}";
}

function validate(events) {
  const errors = [];
  let previous = null;
  let ndfId = null;
  events.forEach((event, index) => {
    if (event.sequence !== index) errors.push("non-contiguous sequence");
    if (event.previous_event_hash !== previous) errors.push("broken previous hash");
    if (ndfId !== null && event.ndf_id !== ndfId) errors.push("ndf_id changed");
    ndfId = event.ndf_id;
    const unsigned = { ...event };
    delete unsigned.event_hash;
    const actual = "sha256:" + createHash("sha256").update(canonicalize(unsigned)).digest("hex");
    if (actual !== event.event_hash) errors.push("incorrect event hash");
    previous = event.event_hash;
  });
  return errors;
}

const file = process.argv[2];
if (!file) throw new Error("usage: node tools/check-custody.mjs <events.json>");
const errors = validate(JSON.parse(readFileSync(file, "utf8")));
for (const error of errors) console.error(error);
process.exitCode = errors.length ? 1 : 0;
