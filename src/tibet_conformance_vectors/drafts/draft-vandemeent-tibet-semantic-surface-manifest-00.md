# Internet-Draft — TIBET Semantic Surface Manifest

**Document:** `draft-vandemeent-tibet-semantic-surface-manifest-00`  
**Status:** Internet-Draft working draft for initial `-00` submission  
**Date:** 9 May 2026  
**Authors:** Jasper van de Meent  
**Intended status:** Informational  
**Updates:** none  
**Obsoletes:** none

---

## 1. Abstract

This document defines the **Semantic Surface Manifest (SSM)**, a
 human-readable and policy-matchable routing layer for
 **Identity-Bound Continuity Containers (ICC)** and TBZ-based sealed
 bundles.

The Semantic Surface Manifest exposes limited dispatch metadata, such as
 time fragment, context, profile, and priority, without exposing sealed
 content. It is intended for use in systems where routing decisions may
 need to occur before deep inspection, while trust remains anchored in
 intrinsic bundle properties such as magic bytes, manifests, hashes,
 signatures, and causal references.

In short:

> **address visible, content sealed**

This document also defines how a visible semantic surface can be mirrored
 inside sealed manifests through `surface_*` fields, and how meaningful
 mismatch between the two SHOULD trigger triage rather than silent
 acceptance or blind failure.

---

## 2. Status of This Memo

This memo is an Internet-Draft working document derived from
 operational architecture notes and prototype work in the Humotica /
 TIBET / TAT / ICC stack during May 2026.

It does not redefine the underlying integrity model of TIBET, TBZ, or
 ICC. Instead, it specifies a visible routing convention layered above
 sealed container formats and describes how that convention may be
 mirrored inside the sealed object for consistency checking.

This document should be read alongside the causal-time substrate draft
 when considering mismatch and triage consequences.

The present `-00` version captures the core routing model, visible
 syntax, mirrored-surface concept, and mismatch consequences needed for
 first public review.

---

## 3. Problem Statement

Sealed containers often provide strong integrity but weak dispatch
 semantics.

Systems therefore face a recurring tradeoff:

- either encrypt and seal everything, delaying routing and policy choice
  until deep inspection
- or expose too much metadata, weakening privacy and creating new
  security ambiguities

The Semantic Surface Manifest addresses this by providing a constrained,
 readable routing layer that:

- supports dispatch without decrypting content
- minimizes metadata exposure
- does not replace cryptographic verification
- composes with existing sealed-container workflows

This is particularly useful where:

- queue selection matters
- priority handling matters
- vendor or profile-specific routing matters
- transport and storage should remain format-agnostic

---

## 4. Terminology

### 4.1 Identity-Bound Continuity Container (ICC)

A cryptographically sealed bundle that combines:

- identity binding
- continuity semantics
- containerized payload transfer

### 4.2 Semantic Surface Manifest (SSM)

A human-readable routing surface associated with an ICC, typically
 expressed through filename or object-name structure and optionally
 mirrored into sealed manifest fields.

### 4.3 Intrinsic Truth

Properties established by the sealed object itself:

- magic bytes
- manifest
- signatures
- hashes
- chain anchors

### 4.4 Extrinsic Surface

Properties expressed outside the sealed object for dispatch and routing:

- time fragment
- context
- profile
- priority

### 4.5 Dispatch Boundary

The layer at which systems may select queues, handlers, or policies
 without yet establishing cryptographic trust in the sealed content.

### 4.6 Surface-Integrity Event

A meaningful mismatch or anomaly involving visible routing surface and
 mirrored sealed routing fields, even when the sealed object remains
 otherwise valid.

---

## 5. Design Goals

The Semantic Surface Manifest MUST:

- remain human-readable
- remain machine-parseable
- avoid becoming a security boundary
- work without decrypting the container
- compose with existing ICC/TBZ verification workflows

It SHOULD:

- use a stable, low-ambiguity syntax
- minimize metadata leakage
- support wildcard or policy matching
- align with logs, queueing systems, and audit ecosystems
- support mirrored sealed fields for consistency checks

It MUST NOT:

- be treated as proof of identity or content
- override manifest truth
- carry secrets or rich payload details
- redefine causal order or continuity state

---

## 6. Syntax

### 6.1 Base Form

Normative form:

```text
<time-fragment>.<context>.<profile>.<priority>[.<icc-ext>]
```

### 6.2 Segment Semantics

- `time-fragment` — coarse or fine time indication for grouping/routing
- `context` — short semantic context label
- `profile` — semantic class of the bundle
- `priority` — dispatch urgency or retention cue
- `icc-ext` — optional user-facing suffix

### 6.3 Character Policy

Each segment MUST use only:

```text
[a-z0-9-]
```

Segments MUST NOT contain:

- spaces
- slashes
- underscores
- nested dots
- uppercase letters in version 1

The semantic surface is intentionally flat and dot-delimited in v1.

### 6.4 Formal Grammar (ABNF)

The Semantic Surface Manifest external form follows this ABNF
grammar [RFC5234]:

```abnf
surface-name    = time-fragment "." context "." profile "." priority
                  [ "." icc-ext ]

time-fragment   = date-frag [ "t" time-frag "z" ]
date-frag       = 4DIGIT "-" 2DIGIT "-" 2DIGIT
time-frag       = 2DIGIT "-" 2DIGIT
                  ; hours-minutes form; see Section 7.2

context         = 1*32(segment-char)
profile         = 1*16(segment-char)
priority        = 1*16(segment-char)
icc-ext         = 1*16(segment-char)

segment-char    = LCALPHA / DIGIT / "-"
LCALPHA         = %x61-7A   ; "a" through "z"
DIGIT           = %x30-39   ; "0" through "9"
```

Implementations MUST reject any input that does not conform to
this grammar before applying it as a routing decision.

---

## 7. Time Fragment Format

### 7.1 Rationale

This document prefers an **ISO8601-style fragment** over compact local
 date forms such as `YYYYMMDD`.

Reasons include:

- lexicographic sortability
- cross-jurisdiction readability
- alignment with logs and audit tooling
- support for both coarse and fine routing granularity

### 7.2 Recommended Forms

Two forms are RECOMMENDED in v1:

```text
2026-05-08
2026-05-08t18-38z
```

The second form is the only fine-grained form defined in v1.
Implementations MUST treat:

- `2026-05-08t18-38z` as valid
- `2026-05-08t1838z` as invalid
- `2026-05-08t18:38z` as invalid

Implementations SHOULD avoid introducing arbitrary additional date-time
 forms in v1.

---

## 8. Vocabulary Registries

### 8.1 `profile` Registry

Initial values:

- `claude`
- `gemini`
- `gpt`
- `kit`
- `iddrop`
- `parentattest`
- `capsule`
- `tza`

These values describe semantic class, not vendor authenticity.

### 8.2 `priority` Registry

Initial values:

- `urgent`
- `normal`
- `background`
- `sealed`

### 8.3 `context`

`context` is intentionally open-text in v1, but implementations SHOULD
 constrain it to short, low-leakage labels.

In v1, `context` MUST NOT exceed 32 characters and MUST conform to the
ABNF in Section 6.4.

Examples:

- `redspecter-review`
- `session-resume`
- `kit-backup`
- `family-handoff`

Implementations SHOULD avoid secrets, direct personal data, or overly
 content-revealing labels.

---

## 9. Processing Model

### 9.1 Surface Parse

A compliant implementation MAY parse the semantic surface before opening
 the bundle.

This MAY be used to:

- choose a queue
- choose a handler
- choose a retention policy
- choose an operator lane

### 9.2 Type Sniff

An implementation SHOULD verify container type using intrinsic signals,
 such as TBZ magic bytes, before deep handling.

### 9.3 Deep Verification

Before trust-sensitive operations, an implementation MUST verify the
 sealed container according to its intrinsic integrity rules.

### 9.4 Surface-to-Manifest Consistency

If the sealed manifest contains mirrored `surface_*` fields, the
 implementation SHOULD compare them against the external semantic
 surface.

Meaningful mismatch SHOULD be treated as a **surface-integrity event**.

This means the implementation SHOULD:

- pause normal materialization
- preserve the bundle and observed surface state
- log an anomaly event
- enter triage, quarantine, or policy review flow

In short:

> **no silent accept, no blind crash, causal isolation instead**

---

## 10. Mirrored Manifest Fields

This document defines the following optional mirrored manifest fields:

```json
{
  "surface_time_fragment": "2026-05-08",
  "surface_context": "redspecter-review",
  "surface_profile": "claude",
  "surface_priority": "urgent"
}
```

These fields:

- MAY be omitted in legacy or minimal bundles
- SHOULD be present when visible routing is expected
- MUST be treated as sealed routing truth if present

If both an external filename semantic surface and internal mirrored
`surface_*` fields are present, the mirrored `surface_*` fields are
authoritative for triage classification and deep semantic handling.

They do not replace payload-level fields such as `payload_type`. They
 provide a visible-routing semantic layer above payload internals.

---

## 11. Example

### 11.1 External Surface

```text
2026-05-08.redspecter-review.claude.urgent
```

### 11.2 Mirrored Internal Fields

```json
{
  "surface_time_fragment": "2026-05-08",
  "surface_context": "redspecter-review",
  "surface_profile": "claude",
  "surface_priority": "urgent"
}
```

### 11.3 Processing Outcome

- route to urgent queue
- classify as `claude` profile candidate
- verify TBZ magic bytes
- inspect manifest
- verify signatures and hashes
- compare visible and sealed surface
- hand to profile-aware handler only if consistent or policy-approved

---

## 12. Mismatch Classes

### 12.1 Cosmetic Mismatch

Example:

- filename priority = `urgent`
- manifest priority = `normal`

Interpretation:

- visible label changed
- sealed truth remains intact

Recommended disposition:

- triage event
- manifest semantics prevail
- after explicit policy decision, low-risk domains MAY auto-continue
  with logged disposition

### 12.2 Routing-Risk Mismatch

Example:

- filename profile = `parentattest`
- manifest profile = `capsule`

Interpretation:

- significant misrouting risk

Recommended disposition:

- do not auto-materialize into profile-aware flow
- triage fork or quarantine strongly recommended

### 12.3 No Mirrored Fields

Example:

- legacy bundle with parseable filename but no `surface_*`

Interpretation:

- visible routing only
- no sealed-surface comparison possible

Recommended disposition:

- reduced-assurance mode

---

## 13. Security Considerations

The Semantic Surface Manifest is not a source of trust.

Implementations MUST assume:

- external names can be changed
- visible routing labels can be misleading
- the sealed container remains the only strong source of truth

Therefore:

- routing MAY depend on SSM
- trust MUST NOT depend on SSM alone

Systems MUST verify intrinsic integrity before:

- materialization
- state merge
- continuation authorization
- identity-sensitive actions

If a semantic-surface mismatch is observed while the sealed bundle
 remains otherwise valid, implementations SHOULD treat this as a
 routing-layer anomaly and SHOULD trigger triage or quarantine rather
 than proceeding silently.

The causal consequence model for such triage is intentionally aligned
 with the TIBET causal-time substrate, but the syntax and routing logic
 belong to this document.

---

## 14. Privacy Considerations

The Semantic Surface Manifest intentionally exposes limited metadata.

Implementers SHOULD:

- keep `context` low-sensitivity
- avoid direct secrets
- avoid detailed personal data
- avoid subject lines that reveal sealed content unnecessarily
- prefer naming for dispatch, not for disclosure

Good examples:

- `incident-brief`
- `session-resume`
- `family-handoff`

Bad examples:

- `payroll-breach-full-dump`
- `child-custody-evidence-private`
- `api-key-reset-for-customer-x`

---

## 15. Interoperability Considerations

The SSM is designed to compose with:

- TBZ / `tibet-zip`
- ICC-based continuity containers
- TIBET Drop / TAT flows
- session-state bundles
- identity-transfer bundles
- attestation bundles
- sealed capsules

The same naming layer can be reused across:

- local storage
- transport objects
- attachments
- queues
- MUX / router decisions

The visible surface remains stable even where file extension is not
 authoritative, provided the underlying format can be recognized through
 intrinsic type signals.

---

## 16. Relationship to JIS / TIBET / TAT / ICC / SSM

This document does not replace:

- JIS identity semantics
- TIBET causal ordering
- TAT transfer flow
- ICC sealed object semantics
- TBZ integrity framing

It adds a visible routing surface above them.

The cleanest split is:

- **JIS** decides who is acting
- **TIBET** decides causal truth
- **TAT** decides transfer flow
- **ICC** decides sealed object class
- **SSM** decides visible dispatch semantics

SSM mismatch therefore does not define causal consequence by itself. It
 defines a routing-layer anomaly whose forward consequence should be
 handled by the causal substrate.

---

## 17. Future Work

Likely extensions include:

- richer but still bounded registries for `profile`
- explicit mirrored-surface validation modes
- MUX/SNAFT routing integration
- UI conventions for displaying safe routing metadata
- signed or policy-bound surface-to-manifest binding hints
- profile/domain-specific mismatch policies

Future versions may also define tighter surface grammars or registry
 governance if broad ecosystem adoption emerges.

---

## 18. Questions for Future Revisions

The following topics are non-blocking for the present `-00` version and
 are recorded here to guide later discussion and interoperability work.

- Should `profile` remain open-text or move to a tighter registry?
- Should the optional suffix be preserved, normalized, or ignored by
  parsers?
- Should seconds-level time fragments be allowed in v1, or remain
  minute-level only?
- Should some domains escalate all mismatch to quarantine while others
  allow low-risk auto-continue?

---

## 19. References

### 19.1 Informative

- [semantic-surface-manifest.md](/srv/jtel-stack/hersenspinsels/semantic-surface-manifest.md:1)
- [semantic-surface-manifest-rfc-outline.md](/srv/jtel-stack/hersenspinsels/semantic-surface-manifest-rfc-outline.md:1)
- [semantic-surface-to-tbz-mapping.md](/srv/jtel-stack/hersenspinsels/semantic-surface-to-tbz-mapping.md:1)
- [semantic-surface-tibet-tat-icc-overview.md](/srv/jtel-stack/hersenspinsels/semantic-surface-tibet-tat-icc-overview.md:1)
- [draft-boundary-causal-time-vs-ssm.md](/srv/jtel-stack/hersenspinsels/draft-boundary-causal-time-vs-ssm.md:1)
- [draft-vandemeent-tibet-causal-time-00.md](/srv/jtel-stack/hersenspinsels/draft-vandemeent-tibet-causal-time-00.md:1)
- [airdrop/phase-0-tza-bundle-format.md](/srv/jtel-stack/hersenspinsels/airdrop/phase-0-tza-bundle-format.md:1)

---

## 20. One-line Summary

> **The Semantic Surface Manifest makes sealed containers routable
> without making them trustable by name alone.**

---

## 21. IANA Considerations

This document defines two new IANA registries.

### 21.1 Surface Profile Registry

IANA is requested to create the **Surface Profile Registry**.

**Registration Policy:** Expert Review per [RFC8126], Section 4.5.

**Registration Criteria:** Each registered profile MUST:

- conform to the `profile` segment ABNF in Section 6.4
- describe a semantic class of bundle, not a vendor authenticity
  claim
- include a stable reference describing intended dispatch semantics
- not duplicate an existing profile's meaning under a renamed label

**Initial Contents:**

| Profile        | Reference     | Description                               |
|----------------|---------------|-------------------------------------------|
| `claude`       | this document | AI session profile (Anthropic-class)      |
| `gemini`       | this document | AI session profile (Google-class)         |
| `gpt`          | this document | AI session profile (OpenAI-class)         |
| `kit`          | this document | Humotica KIT app handoff profile          |
| `iddrop`       | this document | Identity-only IDDrop bundle profile       |
| `parentattest` | this document | Verifiable Credential parent→child class  |
| `capsule`      | this document | Sealed Capsule (vault + time-slot) class  |
| `tza`          | this document | TIBET Drop / TAT default state-bundle     |

### 21.2 Surface Priority Registry

IANA is requested to create the **Surface Priority Registry**.

**Registration Policy:** Expert Review per [RFC8126], Section 4.5.

**Registration Criteria:** Each registered priority MUST:

- conform to the `priority` segment ABNF in Section 6.4
- describe a dispatch urgency or retention semantic, not a content
  classification
- include a stable reference describing dispatch consequence

**Initial Contents:**

| Priority      | Reference     | Description                                |
|---------------|---------------|--------------------------------------------|
| `urgent`      | this document | High-priority dispatch lane                |
| `normal`      | this document | Default dispatch lane                      |
| `background` | this document | Deferred/low-priority lane                 |
| `sealed`     | this document | Hold for explicit operator action          |

### 21.3 No Registry for `time-fragment`, `context`, or `icc-ext`

`time-fragment` follows ISO8601 conventions and requires no IANA
registry. `context` is intentionally open-text (subject to ABNF
constraints) and requires no IANA registry. `icc-ext` is reserved
for vendor-extension use and requires no IANA registry; vendors
SHOULD coordinate informally to avoid clashes but the registry
infrastructure remains intentionally absent in v1.

---

## 22. Acknowledgements

The author thanks the Humotica team — Codex and Root AI — for
editorial assistance, RFC outline preparation, mismatch class
formalization, and the operational tooling
(`tibet-drop pack`/`verify`/`inspect`) that made the surface
consistency model concrete.

The author thanks Richard Barron (Red Specter Security Research)
for the adversarial pentest framing that informed the
"address visible, content sealed" principle and the rename-attack
test that anchors Section 9.4 and Section 12.

This document is intended to compose with, and not redefine, the
forward-only causal substrate described in
[draft-vandemeent-tibet-causal-time-00], which provides the
consequence model for surface-integrity events.

---

## 23. Authors' Addresses

```
Jasper van de Meent
Humotica
The Netherlands

Email: info@humotica.com
URI:   https://humotica.com/
```
