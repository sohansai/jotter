from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Note:
    """Represents a single sticky note or task."""

    id: int
    body: str
    tag: str
    done: bool
    added_at: datetime
    closed_at: datetime | None = None

    def __post_init__(self):
        if not self.body.strip():
            raise ValueError("Note body cannot be empty")
