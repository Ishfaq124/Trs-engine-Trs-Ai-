# TRS v2 Specification

## Definition

A **Temporal Reflective State** is one persisted, bounded cognitive cycle.

A TRS snapshot is an engineering representation of what information was
available, selected, predicted, acted upon, and reflected on at a given time.

## Transition

```text
TRS(t)
  -> observe
  -> retrieve memory
  -> generate workspace candidates
  -> detect contradictions
  -> attention competition
  -> bounded broadcast
  -> predict / reason
  -> act
  -> evaluate
  -> reflect
  -> TRS(t+1)
```

## Identity inertia

A self-model claim stores:

```text
claim
confidence
stability
supporting_evidence[]
counterevidence[]
revision_count
```

The higher the stability, the stronger the evidence required to move confidence.

## Global workspace

Candidate content receives priority based on:

- current relevance
- goal relevance
- salience
- contradiction pressure
- uncertainty
- recency

Only a bounded number of candidates are broadcast to reasoning.

## Temporal lineage

Every state has a `parent_state_id`. This makes questions such as these
answerable:

- Why did a belief change?
- What evidence was active before an action?
- Which state introduced a false belief?
- Did uncertainty fall after information gathering?
