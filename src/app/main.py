import logging

from app.core.logging import setup_logging
from app.scrapers.habr_search import HabrSearchScraper

logger = logging.getLogger("job-radar")


def main() -> None:
    setup_logging("INFO")
    logger.info("Project boot OK")
    #logger.exception("Ошибка при парсинге")

    scraper = HabrSearchScraper(query="python", page=1)
    jobs = scraper.fetch_jobs()

    for j in jobs[:10]:
        logger.info("JOB: %s | %s", j.title, j.url)


if __name__ == "__main__":
    main()
