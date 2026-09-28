import sqlite3

from jotter.infrastructure.database.schema import SCHEMA_V1

CURRENT_VERSION = 1


def run_migrations(conn: sqlite3.Connection) -> None:
    """
    Ensure the database schema is up-to-date.
    Uses PRAGMA user_version to track schema version safely.
    """
    cursor = conn.cursor()
    cursor.execute("PRAGMA user_version")
    version = cursor.fetchone()[0]

    with conn:  # Transaction block
        if version == 0:
            # V1: Initial schema
            conn.executescript(SCHEMA_V1)
            conn.execute(f"PRAGMA user_version = {CURRENT_VERSION}")
            version = 1

        # Future migrations go here:
        # if version == 1:
        #     conn.execute("ALTER TABLE notes ADD COLUMN due_date TEXT")
        #     conn.execute("PRAGMA user_version = 2")
        #     version = 2
