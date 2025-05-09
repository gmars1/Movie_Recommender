FROM python:3.10-slim

WORKDIR /workdir

# Install system + Python deps
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY ./FilmsDatabase ./FilmsDatabase

#RUN pip install -e .
RUN pip install --no-cache-dir -r FilmsDatabase/requirements.txt

# Make entrypoint executable
RUN chmod +x FilmsDatabase/entrypoint.sh

ENTRYPOINT ["/bin/bash", "FilmsDatabase/entrypoint.sh"]