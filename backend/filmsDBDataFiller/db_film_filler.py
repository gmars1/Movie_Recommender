import uuid
from typing import Dict

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from FilmsDatabase.db.database import session_maker
from FilmsDatabase.db.models import Movie, MovieRating, Genre, Actor


def get_or_create_entity(
        session: Session,
        model: type,
        filter_field: str,
        filter_value: str,
        create_data: dict,
        existing_cache: Dict[str, object]
) -> object:
    """Generic function to get or create entities with caching"""
    if filter_value not in existing_cache:
        result = session.execute(
            select(model).where(getattr(model, filter_field) == filter_value)
        )
        entity = result.scalars().first()
        if not entity:
            entity = model(**create_data)
            session.add(entity)
            session.flush()  # Ensure we get the ID if needed
        existing_cache[filter_value] = entity
    return existing_cache[filter_value]


def import_from_excel(file_path: str):
    # Read Excel file
    df = pd.read_excel(file_path, decimal=",")

    # Caches for existing entities
    existing_entities = {
        'genres': {},
        'actors': {}
    }

    with session_maker() as session:
        with session.begin():
            for _, row in df.iterrows():
                # Create Movie
                movie = Movie(
                    id=uuid.uuid4(),
                    title_ru=row['Название (русское)']
                )
                session.add(movie)

                # Create Rating
                rating = MovieRating(
                    movie_id=movie.id,
                    rating=float(row['Рейтинг'])
                )
                session.add(rating)

                # Process Genres
                genre_names = [g.strip() for g in str(row['Жанр']).split(',')]
                for genre_name in genre_names:
                    genre = get_or_create_entity(
                        session=session,
                        model=Genre,
                        filter_field='genre_name',
                        filter_value=genre_name,
                        create_data={
                            'id': uuid.uuid4(),
                            'genre_name': genre_name
                        },
                        existing_cache=existing_entities['genres']
                    )
                    movie.genres.append(genre)

                # Process Actors
                actor_names = [a.strip() for a in str(row['Актеры']).split(',')]
                for actor_name in actor_names:
                    actor = get_or_create_entity(
                        session=session,
                        model=Actor,
                        filter_field='full_name',
                        filter_value=actor_name,
                        create_data={
                            'id': uuid.uuid4(),
                            'full_name': actor_name
                        },
                        existing_cache=existing_entities['actors']
                    )
                    movie.actors.append(actor)

        print(f"Successfully imported {len(df)} movies with relationships")


if __name__ == "__main__":
    import_from_excel("backend/filmsDBDataFiller/top_250.xlsx")
