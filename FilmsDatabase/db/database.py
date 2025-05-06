from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQL_UUID, text
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from FilmsDatabase.db.config import settings

DATABASE_URL = settings.get_db_url()

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")  # For PostgreSQL
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
