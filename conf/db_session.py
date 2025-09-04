from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from models.model_base import ModelBase

__async_engine: AsyncEngine | None = None


def create_engine() -> AsyncEngine:
    """
    Função para configurar a conexão ao banco de dados
    """
    global __async_engine

    if __async_engine:
        return

    url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/picoles'
    __async_engine = create_async_engine(url=url)

    return __async_engine


def create_session() -> AsyncSession:
    """
    Função para criar a sessão de conexão ao banco de dados
    """
    global __async_engine

    if not __async_engine:
        __async_engine = create_engine()

    __async_session = async_sessionmaker(
        bind=__async_engine, class_=AsyncSession, expire_on_commit=False)

    session: AsyncSession = __async_session()

    return session


async def create_tables() -> None:
    global __async_engine

    if not __async_engine:
        __async_engine = create_engine()

    import models.__all__models

    async with __async_engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)
