from __future__ import annotations

from dataclasses import dataclass, field
import time


@dataclass
class BeliefRecord:
    proposition: str
    confidence: float
    evidence: list[str] = field(default_factory=list)
    counterevidence: list[str] = field(default_factory=list)
    last_updated: float = field(default_factory=time.time)


class MetacognitiveLedger:
    def __init__(self):
        self.records: dict[str, BeliefRecord] = {}

    def set(self, key, proposition, confidence, evidence=None, counterevidence=None):
        record = BeliefRecord(
            proposition=proposition,
            confidence=max(0.0, min(1.0, confidence)),
            evidence=evidence or [],
            counterevidence=counterevidence or [],
        )
        self.records[key] = record
        return record

    def uncertainty(self):
        if not self.records:
            return 0.5
        vals = [1.0 - abs(r.confidence - 0.5) * 2.0 for r in self.records.values()]
        return sum(vals) / len(vals)
