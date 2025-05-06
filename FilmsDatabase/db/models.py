from typing import List, Optional
from uuid import UUID

from sqlalchemy import UUID as SQL_UUID, ForeignKey, String, Numeric, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Column

from FilmsDatabase.db.database import Base


class Movie(Base):
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    rating: Mapped[Optional["MovieRating"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
        single_parent=True
    )
    genres: Mapped[List["Genre"]] = relationship(
        secondary="movie_genres",
        back_populates="movies"
    )
    actors: Mapped[List["Actor"]] = relationship(
        secondary="movie_actors",
        back_populates="movies"
    )


class MovieRating(Base):
    movie_id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey('movie.id', ondelete="CASCADE"),
        unique=True
    )
    rating: Mapped[float] = mapped_column(
        Numeric(3, 1),
        nullable=False,
        doc="Rating from 0 to 10"
    )

    # Relationship
    movie: Mapped["Movie"] = relationship(back_populates="rating")


class Genre(Base):
    genre_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    # Relationship
    movies: Mapped[List["Movie"]] = relationship(
        secondary="movie_genres",
        back_populates="genres"
    )


class Actor(Base):
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship
    movies: Mapped[List["Movie"]] = relationship(
        secondary="movie_actors",
        back_populates="actors"
    )


# Association tables with UUID
movie_genres = Table(
    'movie_genres', Base.metadata,
    Column('movie_id', SQL_UUID(as_uuid=True), ForeignKey('movie.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', SQL_UUID(as_uuid=True), ForeignKey('genre.id', ondelete="CASCADE"), primary_key=True)
)

movie_actors = Table(
    'movie_actors', Base.metadata,
    Column('movie_id', SQL_UUID(as_uuid=True), ForeignKey('movie.id', ondelete="CASCADE"), primary_key=True),
    Column('actor_id', SQL_UUID(as_uuid=True), ForeignKey('actor.id', ondelete="CASCADE"), primary_key=True)
)
