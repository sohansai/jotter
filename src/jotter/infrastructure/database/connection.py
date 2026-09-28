import sqlite3
from pathlib import Path


def get_connection(db_path: Path) -> sqlite3.Connection:
    """Provides a configured SQLite connection."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(
        db_path,
        isolation_level=None,  # Autocommit mode
        check_same_thread=False,
    )
    conn.row_factory = sqlite3.Row

    # Apply PRAGMAs
    conn.execute("PRAGMA busy_timeout = 5000")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = 1")

    return conn
