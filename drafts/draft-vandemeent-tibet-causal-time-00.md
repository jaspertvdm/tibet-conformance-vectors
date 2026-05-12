# Internet-Draft — TIBET Causal Time Substrate

**Document:** `draft-vandemeent-tibet-causal-time-00`  
**Status:** Internet-Draft working draft for initial `-00` submission  
**Date:** 9 May 2026  
**Authors:** Jasper van de Meent  
**Intended status:** Informational  
**Updates:** none  
**Obsoletes:** none

---

## 1. Abstract

This document describes the **TIBET Causal Time Substrate**, a
 forward-only causal ordering model for identity-bound distributed
 systems.

TIBET does not treat wall-clock time as the primary ordering primitive.
 Instead, it uses a cryptographically bound logical-time structure,
 encoded through append-only token linkage, monotonic generation
 counters, and signed causal references. External wall-clock sources,
 including NTP, RFC 3161 timestamping services, Roughtime, GNSS, or
 public ledger timestamps, are treated as **auxiliary alignment
 anchors**, not as the constitutive source of event order.

The core claim is simple:

> **TIBET is a forward-only causal substrate that enables recovery and
> reversibility without rewriting history.**

This document positions TIBET relative to Lamport clocks, vector-clock
 traditions, timestamp anchoring systems, and modern off-grid or
 intermittently connected autonomous systems.

---

## 2. Status of This Memo

This memo is an Internet-Draft working document derived from
 operational architecture notes, prototype implementations, and
 forensic delivery work produced in the Humotica / TIBET stack during
 May 2026.

It is intended to capture and formalize an already deployed structural
 property of TIBET rather than to introduce a greenfield timing model.

This document is an initial public framing and substrate document
 intended to align:

- distributed-systems theory
- identity-bound execution
- off-grid or degraded-network operations
- forward-only recovery semantics

---

## 3. Problem Statement

Many distributed systems continue to over-privilege wall-clock time.
 They assume that safe ordering, freshness, replay defense, and
 reversibility can be grounded primarily in synchronized UTC.

That assumption is fragile under:

- intermittent connectivity
- NTP outage or misconfiguration
- GNSS disruption
- clock drift across edge nodes
- compromised or ambiguous time authorities
- adversarial replay after restore or rollback

This document argues that:

- causal order MUST be primary
- wall-clock time SHOULD be auxiliary
- recovery MUST be forward-only
- history MUST NOT be rewritten

In other words, the substrate SHOULD answer "what happened before what"
 before it answers "what time was it globally".

---

## 4. Terminology

### 4.1 Causal Time

The ordering of events by their dependency and sequence relationships,
 rather than by globally synchronized wall-clock timestamps.

### 4.2 Forward-Only Causal Substrate

A substrate in which valid state evolution occurs only by appending new
 causally linked events, and where rollback, reset, amend, or rewind of
 prior committed history is structurally disallowed.

### 4.3 Logical Counter

A monotonic counter associated with event generation and ordering.
 Within TIBET this corresponds to the `generation` field.

### 4.4 External Time Anchor

An observation of an external time-bearing source, recorded into the
 causal substrate as a signed event. It assists alignment but does not
 replace causal ordering.

### 4.5 Drift Record

A signed record describing observed offset between two time-bearing
 participants or between local time and an external anchor.

### 4.6 Triage Fork

A forward-causal isolation path created in response to anomaly,
 mismatch, or uncertain continuity, preserving evidence without
 rewriting prior state.

---

## 5. Design Goals

The TIBET Causal Time Substrate MUST:

- provide forward-only event evolution
- preserve causal ordering without dependence on absolute time
- support cryptographic identity binding of events
- permit recovery, revocation, and compensation without history
  rewriting
- remain meaningful under offline or degraded-network conditions

It SHOULD:

- integrate with external time anchors
- support replay-sensitive freshness checks
- surface time uncertainty honestly
- compose with transfer, fork, merge, tombstone, and audit primitives

It MUST NOT:

- rely on wall-clock synchronization as the sole source of ordering
- permit destructive history rewrite as a normal control path
- treat rollback as equivalent to forward recovery

---

## 6. Model Overview

TIBET encodes causal order through a set of already existing structural
 primitives:

- `prev_token_id`
- hash-linked integrity
- Ed25519 signatures
- `generation`
- `parent_token_id`
- genesis and chain-head semantics

These map naturally onto a Lamport-style logical ordering model:

| TIBET Primitive | Causal-Time Equivalent |
|---|---|
| `prev_token_id` | happened-before pointer |
| hash chain | tamper-evident order proof |
| Ed25519 signature | authenticated event origin |
| `generation` | logical counter |
| `parent_token_id` | causal predecessor |
| genesis marker | event-line root |

The important consequence is that TIBET already behaves as a causally
 ordered logical-time substrate. This document formalizes that fact.

---

## 7. Relation to Lamport and Related Work

This document is directly aligned with:

- Lamport, 1978: *Time, Clocks, and the Ordering of Events in a
  Distributed System*
- Fidge, 1988
- Mattern, 1988

Lamport showed that distributed systems do not require globally
 authoritative time to establish meaningful event order.

TIBET extends that tradition by binding logical ordering to:

- hardware-bound or device-bound identity
- cryptographic signatures
- append-only lineage
- explicit fork / merge / tombstone semantics

This makes TIBET closer to a **signed Lamport substrate** than to a
 timestamp-only logging system.

---

## 8. Forward-Only Property

The defining property of TIBET causal time is not merely that events are
 ordered, but that valid evolution occurs only by moving forward.

This has concrete consequences:

- restore MUST become fork, not rewind
- revocation MUST become successor event, not mutation
- correction MUST become amendment event, not overwrite
- cancellation MUST become compensating action, not erasure

In TIBET terms, history rewriting operations analogous to the following
 are not valid control primitives:

- `reset --hard`
- force-rewrite
- rebase-like history surgery
- destructive rollback

Recovery is therefore expressed causally, not retroactively.

---

## 9. Event Classes

The following event classes are natural inhabitants of the causal-time
 substrate:

- ordinary application or system action tokens
- fork or snapshot-reference events
- merge or transfer-pair events
- tombstone events
- triage or quarantine events
- external time-anchor events
- drift-record events

These classes are not all necessarily already standardized in TIBET
 token type registries, but they align structurally with the substrate
 described here.

---

## 10. External Time Anchors

External time anchors provide auxiliary alignment between local causal
 order and broader time-bearing reference systems.

Possible anchor sources include:

- NTP
- RFC 3161 timestamping authorities
- Roughtime
- GNSS / PTP
- public ledger timestamps
- observed environmental or operational anchors

The crucial rule is:

> **External time anchors MAY improve alignment. They MUST NOT redefine
> already established causal order.**

This avoids a failure mode where a later timestamp authority appears to
 retroactively reorder causally established local history.

---

## 11. Drift and Alignment

Clock drift is expected in real systems, especially edge systems and
 off-grid nodes.

TIBET treats drift as a recordable condition, not as a fatal collapse of
 ordering truth.

Implementations SHOULD be able to represent:

- locally observed time
- externally anchored time
- offset between them
- uncertainty window
- validity scope of the observation

This allows systems to say:

- the local clock believed event X occurred at local time T
- the node was observed to be +14.187 seconds offset from anchor Y
- causal order remains valid regardless

Thus drift becomes auditable and alignable rather than existentially
 destabilizing.

---

## 12. Processing Model

### 12.1 Local Event

When a local event is committed:

- the implementation increments or derives a monotonic generation value
- binds the event to prior causal state
- signs the event

### 12.2 Incoming Causal Reference

When a remote or transferred event enters local reasoning:

- the implementation evaluates causal relation
- MUST derive successor progression in Lamport style as
  `max(local_generation, remote_generation) + 1` for any new local
  successor event that causally depends on both
- MUST preserve observed predecessor linkage

Illustrative pseudocode:

```text
local_generation   = current_chain_head.generation
remote_generation  = incoming_event.generation

successor_generation = max(local_generation, remote_generation) + 1

new_event.prev_token_id   = local_chain_head.token_id
new_event.parent_token_id = incoming_event.token_id
new_event.generation      = successor_generation
sign(new_event)
append(new_event)
```

### 12.3 Recovery

Recovery MUST produce successor state by:

- fork
- compensation
- revocation
- new forward-causal action

It MUST NOT pretend to restore the system to an earlier pre-committed
 causal state.

### 12.4 Time Anchoring

When external time is sampled:

- the implementation MAY write an external-anchor event
- MAY write drift information
- MUST NOT use the anchor to invalidate already committed causal order

---

## 13. Example Flows

### 13.1 Snapshot and Resume

Classical model:

- freeze full state at T
- restore as if time rewound to T

TIBET causal-time model:

- snapshot references a chain position
- resume becomes fork from that position
- new line advances with its own forward-only history

### 13.2 Transfer Pair

In TAT / TIBET Drop:

- `transfer_out` records sender-side causal commitment
- `transfer_in` records receiver-side causal acknowledgement
- successor generation MUST derive from `max(local, sender) + 1`
  for Lamport-compatible logical-clock progression

This is a Lamport-style inheritance event, not just a file transfer.

### 13.3 Semantic Surface Mismatch

If routing surface and sealed manifest differ (see
[draft-vandemeent-tibet-semantic-surface-manifest-00], Section 9.4
and Section 12):

- content may still be valid
- causal substrate SHOULD treat the situation as anomaly
- triage fork or isolation path SHOULD be created

This shows that causality also governs investigation and containment.
The Semantic Surface Manifest document defines the visible-routing
mismatch condition; this document defines the forward-causal
consequence.

---

## 14. Security Considerations

### 14.1 Threat Model

This document assumes an attacker may be able to:

- replay previously valid artifacts
- re-inject old state through backup or restore channels
- manipulate wall-clock sources or exploit clock drift
- rename, relabel, or reorder artifacts outside sealed causal truth
- attempt destructive rollback semantics through operational tooling

This document does NOT assume that all runtimes, kernels, or hardware
 are uncompromisable. Rather, it defines how causal history SHOULD be
 represented so that compromise or recovery does not silently rewrite
 prior truth.

### 14.2 Attacker Capabilities

Representative attacker capabilities include:

- capture and replay of session or transfer artifacts
- replay-after-revoke attempts
- restore of stale snapshots into live context
- backup injection as false recovery
- suppression or concealment of drift conditions
- coercion of operators into trusting wall-clock order over causal order

### 14.3 Primary Risks

The forward-only causal model is specifically designed to reduce:

- replay-after-restore
- session fixation after rollback
- backup injection masquerading as restoration
- silent history erasure
- ambiguity around whether revocation occurred before or after use

### 14.4 Mitigation Matrix

| Threat | Risk | Mitigation in this model |
|---|---|---|
| replay-after-restore | stale valid state reintroduced as live state | restore becomes fork, not rewind |
| replay-after-revoke | old artifact used after invalidation | revocation is forward event; order remains visible |
| backup injection | old backup presented as recovery truth | snapshots are chain-position references, not time rewind |
| clock spoofing | attacker manipulates UTC interpretation | causal order remains primary; anchors are auxiliary |
| drift concealment | stale or misleading freshness claims | drift can be recorded and surfaced as evidence |
| destructive rollback | operator tooling silently mutates history | model disallows history rewrite as valid recovery |

### 14.5 Residual Risks

Implementations remain exposed if they:

- treat wall-clock timestamps as sole freshness source
- allow unsigned or weakly linked state transitions
- hide or suppress drift conditions
- simulate rollback by destructive mutation outside the causal model
- fail to bind successor events to both local and incoming causal state

### 14.6 Security Invariant

The key invariant is:

> **Security-sensitive reversibility MUST be implemented as forward
> causal compensation, not as history rewrite.**

---

## 15. Interoperability Considerations

This substrate is designed to compose with:

- JIS identity
- UPIP continuity
- TAT transfer flow
- TBZ / ICC container semantics
- semantic routing surfaces

It also composes with external time-bearing systems by treating them as
 anchor layers rather than ordering authorities.

Interoperability therefore depends less on UTC agreement and more on:

- shared causal encoding
- verifiable linkage
- explicit anchor semantics
- clear distinction between order and alignment

---

## 16. Relationship to the Broader Humotica Stack

Within the broader architecture:

- **Turing** answers what computes
- **Lamport / causal time** answers when in event order
- **JIS** answers who is permitted
- **SEMA** may answer within what semantic frame

TIBET occupies the causal-time substrate role while composing with the
 other axes.

This document therefore serves as the Lamport-facing half of the
 architectural triad:

- Turing
- Lamport
- JIS

and explains why TIBET is best understood as an identity-bound causal
 substrate rather than as a mere logging chain.

---

## 17. Future Work

Likely extensions include:

- standardized external time-anchor token shape
- standardized drift-record token shape
- explicit uncertainty handling
- causal freshness proofs for intermittently connected devices
- zero-disclosure continuity proofs over long time horizons
- alignment with age/continuity and attestation use cases
- mapping to RFC 3161, Roughtime, and public-ledger anchoring profiles

Further work may also formalize how triage forks, semantic-surface
 anomalies, and continuity proofs fit into a unified causal-time
 registry.

---

## 18. Questions for Future Revisions

The following topics are non-blocking for the present `-00` version and
 are recorded here to guide later discussion and interoperability work.

- Should drift be standardized as its own token type or as a subclass of
  time-anchor event?
- Should external anchor trust levels be formally graded?
- Should causal freshness be defined as a reusable verification
  primitive?
- How should uncertainty and stale-anchor conditions be surfaced in
  operator tooling?
- Should some domains require time-anchor presence while others permit
  purely local causal mode?

---

## 19. References

### 19.1 Normative / Foundational

- Lamport, L. *Time, Clocks, and the Ordering of Events in a
  Distributed System*. Communications of the ACM, 1978.

### 19.2 Informative

- Fidge, C. *Timestamps in Message-Passing Systems That Preserve the
  Partial Ordering*, 1988.
- Mattern, F. *Virtual Time and Global States of Distributed Systems*,
  1988.
- RFC 3161, *Time-Stamp Protocol (TSP)*.
- Roughtime documentation and related research.
- Humotica internal notes:
  - [forward-only-causal-substrate.md](/srv/jtel-stack/hersenspinsels/forward-only-causal-substrate.md:1)
  - [architectural-triad-turing-lamport-jis.md](/srv/jtel-stack/hersenspinsels/architectural-triad-turing-lamport-jis.md:1)
  - [sema-lamport-drift-continuity.md](/srv/jtel-stack/hersenspinsels/sema-lamport-drift-continuity.md:1)
  - [tibet-timeanchor-primitive.md](/srv/jtel-stack/hersenspinsels/tibet-timeanchor-primitive.md:1)

---

## 20. One-line Summary

> **TIBET makes causal order primary, wall-clock time auxiliary, and
> recovery forward-only.**

---

## 21. IANA Considerations

This document has no IANA actions in the present version.

Future revisions MAY define one or more registries for:

- standardized external time-anchor token shapes
  (NTP / RFC 3161 / Roughtime / GNSS / public-ledger)
- standardized drift-record token shapes
- causal freshness proof types

Should such registries be created, the registration policy is
expected to be **Expert Review** per [RFC8126], Section 4.5.

The author requests that any future TIBET-related IANA registry
created under a sibling document cross-reference this document for
the substrate semantics that registered token classes inhabit.

---

## 22. Acknowledgements

The author thanks the Humotica team — Codex and Root AI — for
editorial assistance, internal peer review, and operational tooling
that made this substrate framing concrete rather than theoretical.

The author thanks Richard Barron (Red Specter Security Research)
for adversarial pentest validation that helped sharpen the
forward-only recovery property under realistic attack conditions.

The conceptual lineage of Lamport (1978), Fidge (1988), and
Mattern (1988) is gratefully acknowledged. This document does not
claim novelty in the logical-time model, only in its identity-
bound and signed substrate composition.

---

## 23. Authors' Addresses

```
Jasper van de Meent
Humotica
The Netherlands

Email: info@humotica.com
URI:   https://humotica.com/
```
