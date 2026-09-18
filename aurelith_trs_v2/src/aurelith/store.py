from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .models import MemoryEvent, TRSSnapshot


class Store:
    def __init__(self, path: str):
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(p)

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS memories(
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                content TEXT NOT NULL,
                salience REAL NOT NULL,
                created_at REAL NOT NULL
            )
        """)

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS trs_states(
                id TEXT PRIMARY KEY,
                parent_state_id TEXT,
                cycle INTEGER NOT NULL,
                payload TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS kv(
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        self.db.commit()

    def add_memory(self, m: MemoryEvent) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO memories VALUES(?,?,?,?,?)",
            (m.id, m.kind, m.content, m.salience, m.created_at),
        )
        self.db.commit()

    def recent_memories(self, limit: int = 100) -> list[MemoryEvent]:
        rows = self.db.execute(
            "SELECT id,kind,content,salience,created_at "
            "FROM memories ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [MemoryEvent(*r) for r in rows]

    def save_snapshot(self, s: TRSSnapshot) -> None:
        self.db.execute(
            "INSERT INTO trs_states VALUES(?,?,?,?,?)",
            (s.id, s.parent_state_id, s.cycle, json.dumps(s.to_dict()), s.created_at),
        )
        self.db.commit()

    def latest_snapshot(self) -> dict[str, Any] | None:
        row = self.db.execute(
            "SELECT payload FROM trs_states ORDER BY cycle DESC LIMIT 1"
        ).fetchone()
        return json.loads(row[0]) if row else None

    def set_json(self, key: str, value: Any) -> None:
        self.db.execute(
            "INSERT INTO kv(key,value) VALUES(?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, json.dumps(value)),
        )
        self.db.commit()

    def get_json(self, key: str, default: Any) -> Any:
        row = self.db.execute("SELECT value FROM kv WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else default
