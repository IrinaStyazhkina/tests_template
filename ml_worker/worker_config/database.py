
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from worker_config.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_PSYCOPG,
    echo=False,
    pool_size=5,
    max_overflow=5,
)
session_factory = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass
