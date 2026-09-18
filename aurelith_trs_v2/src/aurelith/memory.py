from __future__ import annotations

import math
import re
import time

from .models import MemoryEvent, uid
from .store import Store


TOKEN = re.compile(r"[A-Za-z0-9_']+")


class MemorySystem:
    def __init__(self, store: Store):
        self.store = store

    @staticmethod
    def tokens(text: str) -> set[str]:
        return {m.group(0).lower() for m in TOKEN.finditer(text)}

    def remember(self, content: str, kind: str = "episode", salience: float = 0.5):
        m = MemoryEvent(
            id=uid("mem"),
            kind=kind,
            content=content,
            salience=max(0.0, min(1.0, salience)),
        )
        self.store.add_memory(m)
        return m

    def recall(self, query: str, limit: int = 8):
        q = self.tokens(query)
        now = time.time()
        scored = []

        for m in self.store.recent_memories(limit=500):
            mt = self.tokens(m.content)
            overlap = len(q & mt) / max(1, len(q))
            age_days = max(0.0, (now - m.created_at) / 86400.0)
            recency = math.exp(-age_days / 60.0)
            score = 0.62 * overlap + 0.25 * m.salience + 0.13 * recency

            if overlap > 0 or m.salience >= 0.85:
                scored.append((score, m))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:limit]
