FROM python:3.10-slim

WORKDIR /workdir

# Install system + Python deps
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY ./backend ./backend
COPY ./FilmsDatabase ./FilmsDatabase
COPY pyproject.toml .

RUN pip install -e .
RUN pip install --no-cache-dir -r backend/filmsDBDataFiller/requirements.txt
RUN pip install --no-cache-dir -r FilmsDatabase/requirements.txt

CMD ["python", "backend/filmsDBDataFiller/main_import.py"]
CMD ["python", "backend/filmsDBDataFiller/db_film_filler.py"]
