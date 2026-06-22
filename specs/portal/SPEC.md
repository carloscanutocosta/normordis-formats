# NORMORDIS Public Verification Portal — Draft 1.0.0

## 1. Scope

The portal is a trusted custody service that resolves a `validation_code`. It
does not make the code itself a signature and does not expose the NDF content.
`openapi.yaml` is the language-neutral machine-readable contract.

## 2. Verification procedure

For every successful lookup the service MUST:

1. resolve the exact NDF custody record without relying on user-supplied
   metadata;
2. recompute JCS and `payload_hash` from the preserved NDF-core;
3. recompute and compare `validation_code`;
4. validate the custody chain and its latest external anchor;
5. validate CAdES, timestamps, revocation material and trust status when
   present;
6. retrieve the current archival state;
7. return separate integrity, authenticity and signature states.

`trusted_custody` means the portal attests that the record was issued and
preserved by the identified institution. It MUST NOT be described as a
personal electronic signature. `integrity_only` MUST NOT be presented as proof
of issuer identity.

## 3. Privacy and abuse resistance

The public response MUST contain only the minimum metadata needed to identify
the document: producing entity, type, finalization date and state. Subject,
recipient, personal identifiers, classification, content and retention details
MUST NOT be exposed by this endpoint.

The service MUST rate-limit enumeration, log abusive access and return the same
not-found response for unknown and non-public records. Logs are subject to a
documented retention period. Public responses MUST NOT be cached when the
document state can change.

## 4. Availability and offline verification

Portal unavailability produces `unavailable`, never `invalid`. Signed or sealed
packages remain independently verifiable offline. Documents authenticated only
by custody require another trusted custody replica or a verifiable exported
custody anchor for offline authenticity.

## 5. Operational trust

The portal operator MUST publish its identity, security contact, incident
policy, supported NDF versions, trust-list update policy and audit history. The
service SHOULD sign API responses or publish a transparency log so that a
response can be evidenced independently of a screenshot.
