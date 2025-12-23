# job-radar

Учебный проект на Python: собирает вакансии с career.habr.com (Хабр Карьера) через парсинг HTML-страницы списка вакансий и фильтрует результаты так, чтобы в выдачу попадали только реальные вакансии.

> Важно: это не официальное API, а HTML-парсинг. Верстка может меняться — селекторы придётся поддерживать.

## Возможности
- Поиск вакансий по строке запроса (`q`) и странице (`page`).
- Фильтрация ссылок: в результат попадают только вакансии вида `/vacancies/<id>`.
- Фильтрация по навыкам из карточки вакансии (блок `vacancy-card__skills`).
- Логирование в консоль.

## Требования
- Python 3.11+ 

## Установка
### macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt


### Windows (PowerShell)
py -m venv .venv
..venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt


## Запуск
python -m app.main


## Настройка поиска
В текущей версии параметры обычно задаются в `app/main.py` (или в месте, где создаётся `HabrSearchScraper`):
- `query` — строка поиска (например, `python`)
- `page` / количество страниц
- `skills_keywords` — ключевые слова для фильтра по skills (например, `junior`, `intern`, `стажер`)


## Структура проекта (пример)
job-radar/
README.md
requirements.txt
app/
main.py
models/
job.py
scrapers/
habr_search.py


## Ограничения и аккуратность
- Не запускай парсер с высокой частотой запросов; добавляй задержки между страницами.
- Если сайт меняет HTML — обновить селекторы в `habr_search.py`.

## Идеи на будущее
- Парсить детальную страницу вакансии (company/location/salary/description).
- Дедупликация и хранение (SQLite).
- Ретраи/бэкофф на временные ошибки сети.

