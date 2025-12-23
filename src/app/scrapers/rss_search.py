from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from app.models.job import Job

logger = logging.getLogger("job-radar")


class RssSearchScraper:
    """
    RSS-скрейпер: получает ленту (XML) и превращает её в список вакансий Job.

    Почему BeautifulSoup:
    - он умеет парсить XML тоже (features="xml")
    - для старта проще, чем отдельные XML-библиотеки
    """

    def __init__(self, feed_url: str, source: str = "rss") -> None:
        self.feed_url = feed_url
        self.source = source

    def fetch_jobs(self) -> list[Job]:
        # timeout нужен всегда: чтобы не зависнуть навсегда на плохой сети
        # follow_redirects=True часто полезно
        with httpx.Client(timeout=15, follow_redirects=True) as client:
            r = client.get(self.feed_url)
            r.raise_for_status()

        soup = BeautifulSoup(r.text, "xml")
        items = soup.select("item")
        logger.info("RSS items found: %s", len(items))

        jobs: list[Job] = []
        for it in items:
            title = (it.title.get_text(strip=True) if it.title else "").strip()
            url = (it.link.get_text(strip=True) if it.link else "").strip()
            pub_date_raw = it.pubDate.get_text(strip=True) if it.pubDate else None

            published_at = self._parse_rfc822(pub_date_raw)

            # В RSS не всегда есть company/location как отдельные поля —
            # оставим None, а позже будем обогащать.
            jobs.append(
                Job(
                    source=self.source,
                    title=title,
                    url=url,
                    company=None,
                    location=None,
                    published_at=published_at,
                )
            )

        return jobs

    @staticmethod
    def _parse_rfc822(value: Optional[str]) -> Optional[datetime]:
        # В RSS даты часто в формате RFC822, например:
        # "Sat, 20 Dec 2025 10:15:00 +0300"
        # На старте сделаем простой парсинг: если не получилось — вернём None.
        if not value:
            return None
        try:
            # datetime.strptime не всегда понимает все варианты timezone,
            # поэтому на старте допускаем fallback в None.
            return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z")
        except Exception:
            return None
