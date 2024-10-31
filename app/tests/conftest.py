import os
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.api.db_utils.db_connect import Base, get_async_session
from app.main import app

DATABASE_URL: str = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres"
DATABASE_URL_TEST = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/test_db"



async def create_test_database():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute("CREATE DATABASE test_db")
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

async def drop_test_database():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute("DROP DATABASE IF EXISTS test_db WITH (FORCE)")
    await engine.dispose()

@pytest.fixture(scope="session", autouse=True)
def test_database():
    try:
        asyncio.run(create_test_database())
    except ProgrammingError:
        print("Тестовая БД уже существует.")
    yield 
    asyncio.run(drop_test_database())

@pytest.fixture
def app_with_test_db():
    def get_test_session():
        engine_test = create_async_engine(DATABASE_URL_TEST)
        session_local_test = async_sessionmaker(bind=engine_test, class_=AsyncSession)
        return session_local_test()
    app.dependency_overrides[get_async_session] = get_test_session
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
async def async_client(app_with_test_db):
    async with AsyncClient(app=app_with_test_db, base_url="http://localhost:8000") as client:
        yield client