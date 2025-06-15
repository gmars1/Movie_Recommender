FROM python:3.10-slim

WORKDIR /app

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
 
COPY ./backend/filmsDBDataFiller/run_seeder.sh /app/run_seeder.sh
RUN chmod +x /app/run_seeder.sh # Исправлен путь для chmod

# Эта команда будет выполнена при запуске контейнера
CMD ["sh", "-c", "echo 'Starting seeder...' && \
     if [ -f /app/run_seeder.sh ]; then \
         /app/run_seeder.sh; \
     fi"]