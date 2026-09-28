SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS notes (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    body      TEXT    NOT NULL,
    tag       TEXT    NOT NULL DEFAULT '',
    done      INTEGER NOT NULL DEFAULT 0,
    added_at  TEXT    NOT NULL,
    closed_at TEXT
);
CREATE INDEX IF NOT EXISTS notes_open_idx ON notes (done, added_at);
CREATE INDEX IF NOT EXISTS notes_tag_idx  ON notes (tag) WHERE tag <> '';
"""
