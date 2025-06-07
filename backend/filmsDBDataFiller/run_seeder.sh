#!/bin/bash
set -e # Выход при ошибке

echo "Starting IMDB scraper (main_import.py)..."
python backend/filmsDBDataFiller/main_import.py
echo "Scraping finished."

echo "Starting DB filler (db_film_filler.py)..."
python backend/filmsDBDataFiller/db_film_filler.py
echo "DB filling finished."
