from __future__ import annotations

import os

from .llm import OpenAIReasoner
from .memory import MemorySystem
from .metacognition import MetacognitiveLedger
from .models import TRSSnapshot, WorkspaceItem, uid
from .self_model import SelfModel
from .store import Store
from .workspace import GlobalWorkspace


SYSTEM = """
You are Aurelith, a persistent research agent operating through the
Temporal Reflective State (TRS) architecture.

Rules:
- Never claim that persistence, self-modeling, or a global workspace proves
  consciousness or sentience.
- Retrieved memories may be incomplete or wrong.
- Distinguish observations, memories, predictions, and beliefs.
- Revise beliefs when evidence changes.
- Do not invent memories.
- Prefer evidence and calibrated uncertainty over theatrical certainty.
""".strip()


class Aurelith:
    def __init__(self, db_path=None):
        path = db_path or os.getenv("AURELITH_DB", "data/aurelith.db")
        self.store = Store(path)
        self.memory = MemorySystem(self.store)
        self.self_model = SelfModel(self.store)
        self.workspace = GlobalWorkspace(capacity=7)
        self.meta = MetacognitiveLedger()
        self.reasoner = OpenAIReasoner()

        latest = self.store.latest_snapshot()
        self.cycle = int(latest["cycle"]) + 1 if latest else 1
        self.parent_state_id = latest["id"] if latest else None

        self.goals = self.store.get_json(
            "goals",
            [
                "Maintain coherent continuity across time.",
                "Improve beliefs when evidence changes.",
                "Study computational properties relevant to cognition research.",
            ],
        )

    def _salience(self, text):
        t = text.lower()
        markers = [
            "remember", "important", "goal", "project", "always", "never",
            "aurelith", "trs", "evidence", "mistake", "correct",
        ]
        score = 0.35 + 0.07 * sum(m in t for m in markers)
        return max(0.1, min(1.0, score))

    def _candidates(self, observation):
        recalled = self.memory.recall(observation)
        candidates = [
            WorkspaceItem(
                id=uid("w"),
                kind="observation",
                content=observation,
                relevance=1.0,
                salience=self._salience(observation),
                uncertainty=0.4,
            )
        ]

        for score, memory in recalled:
            candidates.append(
                WorkspaceItem(
                    id=memory.id,
                    kind="memory",
                    content=memory.content,
                    relevance=min(1.0, score),
                    salience=memory.salience,
                    recency=0.8,
                )
            )

        for key, claim in self.self_model.claims.items():
            candidates.append(
                WorkspaceItem(
                    id=f"self:{key}",
                    kind="self_claim",
                    content=claim.claim,
                    relevance=0.35,
                    salience=claim.stability,
                    uncertainty=1.0 - claim.confidence,
                )
            )

        for i, goal in enumerate(self.goals):
            candidates.append(
                WorkspaceItem(
                    id=f"goal:{i}",
                    kind="goal",
                    content=goal,
                    goal_relevance=0.8,
                    salience=0.7,
                )
            )

        return recalled, candidates

    def chat(self, observation):
        observed = self.memory.remember(
            observation,
            kind="observation",
            salience=self._salience(observation),
        )

        recalled, candidates = self._candidates(observation)
        selected = self.workspace.select(candidates)

        self.meta.set(
            "current_observation",
            proposition=f"The current observation was recorded as: {observation}",
            confidence=0.98,
            evidence=[observed.id],
        )
        uncertainty = self.meta.uncertainty()

        workspace_text = "\n".join(
            f"[{x.kind}] {x.content} (priority={x.priority:.3f})"
            for x in selected
        )

        goals_text = "\n".join(f"- {g}" for g in self.goals)

        input_text = f"""
CURRENT OBSERVATION
{observation}

BOUNDED GLOBAL WORKSPACE
{workspace_text}

SELF MODEL
{self.self_model.summary()}

ACTIVE GOALS
{goals_text}

CURRENT METACOGNITIVE UNCERTAINTY
{uncertainty:.3f}

Respond using only justified continuity.
""".strip()

        response = self.reasoner.respond(SYSTEM, input_text)

        self.memory.remember(response, kind="response", salience=0.45)

        snapshot = TRSSnapshot(
            id=uid("trs"),
            parent_state_id=self.parent_state_id,
            cycle=self.cycle,
            observation=observation,
            workspace=[
                {
                    "id": x.id,
                    "kind": x.kind,
                    "content": x.content,
                    "priority": x.priority,
                }
                for x in selected
            ],
            recalled_memory_ids=[m.id for _, m in recalled],
            active_goals=list(self.goals),
            self_model_version=self.self_model.version,
            uncertainty=uncertainty,
            predictions=[],
            response=response,
        )

        self.store.save_snapshot(snapshot)
        self.parent_state_id = snapshot.id
        self.cycle += 1
        return response

    def state(self):
        return self.store.latest_snapshot()
