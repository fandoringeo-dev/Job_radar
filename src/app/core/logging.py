import logging
import sys

# Базовая настройка логов для всего проекта.
# В реальном проекте логи — это "черный ящик": что случилось, где, когда.
def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
        #handlers=[logging.FileHandler("app.log")] - Если нужно записать логи в файл
    )
