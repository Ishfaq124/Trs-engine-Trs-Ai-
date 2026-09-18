# Aurelith / TRS Cognitive Architecture

**Aurelith** is the persistent agent identity.

**TRS (Temporal Reflective State)** is the cognitive architecture that constructs,
links, evaluates, and persists Aurelith's bounded internal states over time.

This is a research prototype. It does **not** claim that Aurelith is conscious or
sentient. The goal is to implement and test computational properties discussed
in cognitive-architecture and machine-consciousness research.

## Core idea

```text
prompt -> model -> answer
```

becomes:

```text
perception
   |
   v
episodic / semantic / procedural memory
   |
   v
evidence-linked self-model
   |
   v
bounded global workspace
   |
   v
world-model prediction + deliberation
   |
   v
action
   |
   v
metacognition + reflection
   |
   v
new TRS state -> persisted lineage
```

Each cycle creates a TRS snapshot:

```text
TRS(t) = {
  observation,
  workspace,
  recalled_memory,
  active_goals,
  self_model_version,
  uncertainty,
  predictions,
  response,
  reflection,
  parent_state_id
}
```

## Research differentiators

1. **Temporal state lineage**
   Every cognitive cycle is stored as a state descended from the previous state.

2. **Evidence-linked self-model revision**
   Claims about identity or capabilities do not freely rewrite themselves.

3. **Identity inertia**
   High-stability identity claims require stronger evidence to change than
   ordinary capability estimates.

4. **Bounded global workspace**
   Memories, goals, contradictions, predictions, and observations compete for a
   limited attention budget.

5. **Metacognitive belief ledger**
   Important beliefs track confidence, evidence, counterevidence, and revision.

## Implemented in v0.2

- persistent SQLite event/state storage
- temporal TRS snapshots
- episodic memories
- evidence-linked self-model claims
- bounded workspace selection
- confidence / uncertainty tracking
- OpenAI Responses API adapter
- CLI
- structural tests for workspace bounds, identity inertia, and state lineage

## Quick start

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -e .[dev]
```

Create `.env` from `.env.example` and set:

```env
OPENAI_API_KEY=your_key_here
AURELITH_MODEL=gpt-5.6
```

Run:

```bash
aurelith
```

Tests:

```bash
pytest
```

## Scientific position

Memory, self-modeling, a global workspace, predictive processing, or reflection
do not by themselves prove phenomenal consciousness.

See:
- `docs/TRS_SPEC.md`
- `docs/CONSCIOUSNESS_RESEARCH.md`
- `docs/RESEARCH_LANDSCAPE.md`
- `docs/RESEARCH_QUESTIONS.md`
