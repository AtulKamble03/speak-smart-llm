import json
import sqlite3
from datetime import datetime
from pathlib import Path

from analyzer import AnalysisResult


class SessionHistorian:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp       DATETIME DEFAULT CURRENT_TIMESTAMP,
                    raw_input       TEXT NOT NULL,
                    filler_count    INTEGER,
                    grammar_errors  INTEGER,
                    clarity_score   REAL,
                    fluency_score   REAL,
                    overall_score   REAL,
                    rewritten_text  TEXT,
                    suggestions     TEXT,
                    filler_words    TEXT
                )
            """)

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def save_session(self, result: AnalysisResult) -> int:
        with self._conn() as conn:
            cursor = conn.execute(
                """INSERT INTO sessions
                   (raw_input, filler_count, grammar_errors, clarity_score,
                    fluency_score, overall_score, rewritten_text, suggestions, filler_words)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    result.raw_input,
                    result.filler_word_count,
                    len(result.grammar_errors),
                    result.clarity_score,
                    result.fluency_score,
                    result.overall_score,
                    result.rewritten_text,
                    json.dumps(result.suggestions),
                    json.dumps(result.filler_words_found),
                ),
            )
            return cursor.lastrowid

    def get_all_sessions(self) -> list[dict]:
        with self._conn() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM sessions ORDER BY timestamp DESC"
            ).fetchall()
        sessions = []
        for row in rows:
            s = dict(row)
            s["suggestions"] = json.loads(s["suggestions"] or "[]")
            s["filler_words"] = json.loads(s["filler_words"] or "[]")
            sessions.append(s)
        return sessions

    def get_trend_data(self) -> dict:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT timestamp, overall_score, filler_count, grammar_errors FROM sessions ORDER BY timestamp ASC"
            ).fetchall()
        timestamps = [r[0] for r in rows]
        scores = [r[1] for r in rows]
        filler_counts = [r[2] for r in rows]
        grammar_counts = [r[3] for r in rows]
        return {
            "timestamps": timestamps,
            "scores": scores,
            "filler_counts": filler_counts,
            "grammar_counts": grammar_counts,
        }

    def clear_history(self):
        with self._conn() as conn:
            conn.execute("DELETE FROM sessions")
