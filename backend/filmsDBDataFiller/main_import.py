import asyncio
import json

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

MAX_MOVIES = 50 # Изменяем на 50 для тестирования
CONCURRENT_REQUESTS = 5  # Ограничиваем количество одновременных запросов
REQUEST_DELAY = 0.2  # Задержка перед каждым запросом (в секундах)

semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

async def get_actors(session, movie_url):
    try:
        async with semaphore:  # Ограничиваем количество одновременных запросов
            await asyncio.sleep(REQUEST_DELAY)  # Задержка перед запросом
            async with session.get(movie_url, headers=HEADERS) as response:
                response.raise_for_status()
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

            ld_json_script = soup.find('script', type='application/ld+json')
            if not ld_json_script:
                return "Актеры не найдены"

            data = json.loads(ld_json_script.string)
            actors = data.get('actor', [])
            actor_names = [actor.get('name', '') for actor in actors[:15]]
            return ', '.join(actor_names) if actor_names else "Актеры не найдены"
    except aiohttp.ClientResponseError as e:
        print(f"Ошибка при получении актеров с {movie_url}: {e}")
        return "Ошибка"
    except Exception as e:
        print(f"Общая ошибка при получении актеров с {movie_url}: {e}")
        return "Ошибка"

async def fetch_movie_data(session, idx, item):
    base_url = item.get('url', '')
    if base_url.startswith('http'):
        movie_url = f"{base_url}?ref_=chttp_t_{idx}"
    else:
        movie_url = f"https://www.imdb.com{base_url}?ref_=chttp_t_{idx}"

    print(f"Обрабатываем фильм {idx}: {item.get('alternateName', '')} - {movie_url}")

    actors = await get_actors(session, movie_url)
    print(f"{idx} Найденные актеры: {actors}\n")

    return {
        'Название (русское)': item.get('alternateName', ''),
        'Рейтинг': item.get('aggregateRating', {}).get('ratingValue', ''),
        'Жанр': item.get('genre', ''),
        'Актеры': actors
    }

async def fetch_imdb_top_250():
    url = "https://www.imdb.com/chart/top/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                response.raise_for_status()
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

            ld_json_script = soup.find('script', type='application/ld+json')
            if not ld_json_script:
                print("Не найден блок с JSON-данными на странице топ-250")
                return

            data = json.loads(ld_json_script.string)
            if data.get('@type') != 'ItemList':
                print("JSON не содержит ItemList")
                return

            tasks = []
            for idx, entry in enumerate(data['itemListElement'], start=1):
                if idx > MAX_MOVIES:
                    break
                item = entry['item']
                task = asyncio.create_task(fetch_movie_data(session, idx, item))
                tasks.append(task)

            movies = await asyncio.gather(*tasks)

        df = pd.DataFrame(movies)
        df.to_excel('top_250.xlsx', index=False)
        print("Данные успешно сохранены в top_250.xlsx")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_imdb_top_250())
