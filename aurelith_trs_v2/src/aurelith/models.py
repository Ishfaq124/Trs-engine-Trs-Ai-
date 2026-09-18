from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
import time
import uuid


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass
class Evidence:
    id: str
    text: str
    weight: float
    source: str
    created_at: float = field(default_factory=time.time)


@dataclass
class SelfClaim:
    id: str
    claim: str
    confidence: float
    stability: float
    supporting_evidence: list[str] = field(default_factory=list)
    counterevidence: list[str] = field(default_factory=list)
    revision_count: int = 0
    updated_at: float = field(default_factory=time.time)


@dataclass
class MemoryEvent:
    id: str
    kind: str
    content: str
    salience: float
    created_at: float = field(default_factory=time.time)


@dataclass
class WorkspaceItem:
    id: str
    kind: str
    content: str
    relevance: float = 0.0
    goal_relevance: float = 0.0
    salience: float = 0.0
    contradiction: float = 0.0
    uncertainty: float = 0.0
    recency: float = 1.0

    @property
    def priority(self) -> float:
        return (
            0.30 * self.relevance
            + 0.18 * self.goal_relevance
            + 0.16 * self.salience
            + 0.18 * self.contradiction
            + 0.12 * self.uncertainty
            + 0.06 * self.recency
        )


@dataclass
class TRSSnapshot:
    id: str
    parent_state_id: str | None
    cycle: int
    observation: str
    workspace: list[dict[str, Any]]
    recalled_memory_ids: list[str]
    active_goals: list[str]
    self_model_version: int
    uncertainty: float
    predictions: list[str]
    response: str
    reflection: str = ""
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
