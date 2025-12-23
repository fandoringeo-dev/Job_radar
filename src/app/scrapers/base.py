from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class RawJob:
    # Минимальный набор, который почти всегда можно достать со списка вакансий
    source: str          # например "habr", "hh", "company_site"
    title: str
    url: str
    company: str | None = None
    location: str | None = None
    published_at: datetime | None = None


class Scraper(Protocol):
    # Единый интерфейс: любой источник должен уметь вернуть список вакансий
    def fetch_jobs(self) -> list[RawJob]:
        pass
