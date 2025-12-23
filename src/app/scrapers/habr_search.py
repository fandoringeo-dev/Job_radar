import logging
from urllib.parse import urlencode, urljoin

import httpx
from bs4 import BeautifulSoup

from app.models.job import Job
import re

VACANCY_RE = re.compile(r"^/vacancies/\d+$")
SKILL_KEYWORDS = ("стажер", "стажёр", "intern", "junior")
logger = logging.getLogger("job-radar")


class HabrSearchScraper:
    """
    Поиск вакансий на Хабр Карьере через HTML список вакансий.

    Важно:
    - Это НЕ API, а парсинг HTML, поэтому верстка может меняться.
    - Мы делаем аккуратный запрос: таймаут, User-Agent, без бешеной частоты.
    """

    BASE_URL = "https://career.habr.com"
    SEARCH_PATH = "/vacancies"

    def __init__(self, query: str, page: int = 1) -> None:
        self.query = query
        self.page = page

    def fetch_jobs(self) -> list[Job]:
        url = self._build_url()

        headers = {
            "User-Agent": "job-radar/0.1 (+https://github.com/yourname/job-radar)",
            "Accept-Language": "ru,en;q=0.9",
        }

        with httpx.Client(timeout=15, follow_redirects=True, headers=headers) as client:
            r = client.get(url)
            r.raise_for_status()

        soup = BeautifulSoup(r.text, "lxml")

        job_links = soup.select('a[href^="/vacancies/"]')

        jobs: list[Job] = []
        seen = set()

        for a in job_links:
            href = a.get("href")
            title = a.get_text(strip=True)

            if not href or not title:
                continue

            # Оставляем только реальные вакансии вида /vacancies/123456
            if not VACANCY_RE.match(href):
                continue

            # Поднимаемся до контейнера, внутри которого есть skills
            card = a.find_parent(lambda tag: tag and tag.select_one(".vacancy-card__skills"))
            if not card:
                continue

            skills_block = card.select_one(".vacancy-card__skills")
            # Собираем все “чипы” навыков текстом
            skills_text = " ".join(s.strip().lower() for s in skills_block.stripped_strings)

            # Фильтр: ключевые слова должны встретиться в skills
            if not any(k in skills_text for k in SKILL_KEYWORDS):
                continue

            key = (title, href)
            if key in seen:
                continue
            seen.add(key)

            full_url = urljoin(self.BASE_URL, href)

            jobs.append(
                Job(
                    source="habr_career",
                    title=title,
                    url=full_url,
                    company=None,
                    location=None,
                    published_at=None,
                )
            )




        logger.info(
            "Habr jobs parsed: %s (query=%r page=%s)",
            len(jobs),
            self.query,
            self.page,
        )
        return jobs


    def _build_url(self) -> str:
        # Строим URL поиска.
        # На многих сайтах параметр query называется q, query, search и т.п.
        # Тут мы делаем наиболее распространённый вариант.
        params = {"q": self.query, "page": self.page}
        return f"{self.BASE_URL}{self.SEARCH_PATH}?{urlencode(params)}"
