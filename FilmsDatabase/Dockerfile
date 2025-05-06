FROM python:3.10-slim

WORKDIR /FilmsDatabase

ENV PYTHONPATH="/FilmsDatabase/.."

# Install system + Python deps
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY . .

#RUN pip install -e .
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]