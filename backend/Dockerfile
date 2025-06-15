# Dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /app

# Установка зависимостей ОС, если нужны (например, для psycopg2)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./recommender_service/requirements.txt /app/recommender_service/requirements.txt
RUN ls -la recommender_service/requirements.txt  # Проверка, что файл на месте
RUN pip install --no-cache-dir -r recommender_service/requirements.txt

# Копируем код Django-приложения
# Убедись, что manage.py и папка core (с settings.py) оказываются в /app

#COPY ./backend/manage.py /app/manage.py
#COPY ./backend/core /app/core
#COPY ./backend/films /app/films
COPY ./backend /app/backend
# Если есть другие приложения Django, их тоже нужно скопировать

COPY ./recommender_service/recommender.py /app/recommender_service/recommender.py

# Команда по умолчанию (может быть переопределена в docker-compose.yml)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
