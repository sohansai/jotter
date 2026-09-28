import os
from pathlib import Path

from platformdirs import user_data_dir


def get_db_path() -> Path:
    """
    Get the path to the Jotter SQLite database.
    Honours JOTTER_DB, then checks platform-specific user data directory.
    """
    env_path = os.getenv("JOTTER_DB")
    if env_path:
        return Path(env_path)

    new_dir = Path(user_data_dir("jotter"))
    new_db = new_dir / "jotter.db"

    # Default to new DB
    return new_db
