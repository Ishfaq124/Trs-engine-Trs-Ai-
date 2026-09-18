from __future__ import annotations

import time

from .models import Evidence, SelfClaim
from .store import Store


class SelfModel:
    KEY = "self_model"

    def __init__(self, store: Store):
        self.store = store
        raw = store.get_json(self.KEY, None)

        if raw is None:
            self.version = 1
            self.claims = {
                "identity": SelfClaim(
                    id="identity",
                    claim="I am Aurelith, a persistent TRS research agent.",
                    confidence=0.95,
                    stability=0.95,
                ),
                "consciousness": SelfClaim(
                    id="consciousness",
                    claim=(
                        "My architecture may implement consciousness-related "
                        "computational indicators, but subjective experience is unproven."
                    ),
                    confidence=0.99,
                    stability=0.98,
                ),
            }
            self._persist()
        else:
            self.version = raw["version"]
            self.claims = {k: SelfClaim(**v) for k, v in raw["claims"].items()}

    def _persist(self):
        self.store.set_json(
            self.KEY,
            {
                "version": self.version,
                "claims": {k: vars(v) for k, v in self.claims.items()},
            },
        )

    def propose_claim(self, key: str, claim: str, confidence=0.5, stability=0.5):
        if key in self.claims:
            return self.claims[key]

        self.claims[key] = SelfClaim(
            id=key,
            claim=claim,
            confidence=max(0.0, min(1.0, confidence)),
            stability=max(0.0, min(1.0, stability)),
        )
        self.version += 1
        self._persist()
        return self.claims[key]

    def apply_evidence(self, key: str, evidence: Evidence, supports: bool):
        claim = self.claims[key]

        if supports:
            claim.supporting_evidence.append(evidence.id)
            direction = 1.0
        else:
            claim.counterevidence.append(evidence.id)
            direction = -1.0

        learning_rate = 0.22 * (1.0 - 0.82 * claim.stability)
        delta = direction * learning_rate * max(0.0, min(1.0, evidence.weight))

        old = claim.confidence
        claim.confidence = max(0.01, min(0.99, claim.confidence + delta))

        if abs(claim.confidence - old) >= 0.01:
            claim.revision_count += 1
            claim.updated_at = time.time()
            self.version += 1

        self._persist()
        return claim

    def summary(self):
        return "\n".join(
            f"- {k}: {c.claim} [confidence={c.confidence:.2f}, stability={c.stability:.2f}]"
            for k, c in self.claims.items()
        )
