# Tiny on-device note memory - one SQLite file, no server, no cloud.
import sqlite3
import time
from pathlib import Path

DB_PATH = Path("focusflow.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at REAL,
        source TEXT,
        transcript TEXT,
        summary TEXT,
        keywords TEXT
    )""")
    return conn


def save_session(source, transcript, summary, keywords):
    # Store 1 processed note. keywords is a list -> saved as comma text.
    conn = _connect()
    conn.execute(
        "INSERT INTO sessions (created_at, source, transcript, summary, keywords)"
        " VALUES (?, ?, ?, ?, ?)",
        (time.time(), source, transcript, summary, ", ".join(keywords)),
    )
    conn.commit()
    conn.close()


def list_sessions(limit=20):
    # Return recent notes, newest 1st (id, date string, source, summary preview).
    conn = _connect()
    rows = conn.execute(
        "SELECT id, created_at, source, substr(summary, 1, 80)"
        " FROM sessions ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [
        {"id": r[0], "date": time.strftime("%Y-%m-%d %H:%M", time.localtime(r[1])),
         "source": r[2], "preview": r[3]}
        for r in rows
    ]


def get_session(session_id):
    # Return one full note.
    conn = _connect()
    row = conn.execute(
        "SELECT transcript, summary, keywords FROM sessions WHERE id = ?",
        (session_id,),
    ).fetchone()
    conn.close()
    if not row:
        return None
    return {"transcript": row[0], "summary": row[1], "keywords": row[2]}