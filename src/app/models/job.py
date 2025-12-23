from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Job:
    source: str
    title: str
    url: str
    company: str | None
    location: str | None
    published_at: datetime | None
