from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQL_UUID, text, create_engine
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, sessionmaker

from FilmsDatabase.db.config import settings

DATABASE_URL = settings.get_db_url()

# Создаем синхронный движок для работы с базой данных
engine = create_engine(url=DATABASE_URL)
# Создаем фабрику сессий для взаимодействия с базой данных
session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")  # For PostgreSQL
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        nullable=True  # Разрешаем NULL
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True  # Разрешаем NULL
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
