from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


class SQLiteConversationMemory:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages(session_id, id);

                CREATE TABLE IF NOT EXISTS facts (
                    session_id TEXT NOT NULL,
                    fact_key TEXT NOT NULL,
                    fact_value TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY(session_id, fact_key)
                );
                """
            )

    def add_message(self, session_id: str, role: str, content: str) -> None:
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO messages(session_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, role, content, datetime.now(timezone.utc).isoformat()),
            )

    def history(self, session_id: str, limit: int = 20) -> list[dict[str, str]]:
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT role, content, created_at
                FROM messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, limit),
            ).fetchall()
        return [dict(row) for row in reversed(rows)]

    def upsert_fact(self, session_id: str, key: str, value: str) -> None:
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO facts(session_id, fact_key, fact_value, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(session_id, fact_key)
                DO UPDATE SET fact_value = excluded.fact_value,
                              updated_at = excluded.updated_at
                """,
                (session_id, key, value, datetime.now(timezone.utc).isoformat()),
            )

    def facts(self, session_id: str) -> dict[str, str]:
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT fact_key, fact_value
                FROM facts
                WHERE session_id = ?
                """,
                (session_id,),
            ).fetchall()
        return {row["fact_key"]: row["fact_value"] for row in rows}

    def clear(self, session_id: str) -> None:
        with self._connection() as connection:
            connection.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            connection.execute("DELETE FROM facts WHERE session_id = ?", (session_id,))
