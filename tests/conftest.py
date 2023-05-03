import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_db
from src.main import app
from src.database import Base
from src.security import Hasher
from src.users.models import User, City
from src.users.dals import UserDAL


metadata = Base.metadata

DATABASE_URL_TEST = f"postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_user():
    password = "admin"
    user_data = {
        "first_name": "admin",
        "last_name": "admin",
        "other_name": "admin",
        "email": "admin@admin.ru",
        "is_admin": True,
        "hashed_password": Hasher.get_password_hash(password)
    }

    async def create_admin_user():
        async with async_session_maker() as session:
            user_dal = UserDAL(session)
            admin_user = await user_dal.create_user(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                other_name=user_data["other_name"],
                email=user_data["email"],
                is_admin=user_data["is_admin"],
                hashed_password=user_data["hashed_password"],
                city=None,
                additional_info=None,
                birthday=None,
                phone=None,
            )

            await session.commit()
            await session.refresh(admin_user)
            return admin_user
    admin = await create_admin_user()
    yield admin, user_data, password
    async with async_session_maker() as session:
        await session.execute(delete(User).where(User.email == "admin@admin.ru"))
        await session.commit()


@pytest.fixture
async def authorized_admin_client(admin_user):
    admin, user_data, password = admin_user
    login_data = {
        "login": user_data["email"], "password": password
    }
    login_response = client.post(
        "/login",
        json=login_data
    )
    assert login_response.status_code == 200
    assert "Authorization" in login_response.cookies
    token_value = login_response.cookies["Authorization"]
    assert token_value is not None
    assert token_value.strip('"').startswith("Bearer")

    cookies = {"Authorization": token_value}
    yield cookies, admin, user_data, password


@pytest.fixture
async def user():
    password = "user"
    user_data = {
        "first_name": "user",
        "last_name": "user",
        "other_name": "user",
        "email": "user@user.ru",
        "is_admin": False,
        "hashed_password": Hasher.get_password_hash(password)
    }

    async def create_user():
        async with async_session_maker() as session:
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                other_name=user_data["other_name"],
                email=user_data["email"],
                is_admin=user_data["is_admin"],
                hashed_password=user_data["hashed_password"],
                city=None,
                additional_info=None,
                birthday=None,
                phone=None,
            )

            await session.commit()
            await session.refresh(user)
            return user

    user = await create_user()
    yield user, user_data, password
    async with async_session_maker() as session:
        await session.execute(
            delete(User).where(User.email == "user@user.ru"))
        await session.commit()


@pytest.fixture
async def authorized_user_client(user):
    user, user_data, password = user
    login_data = {
        "login": user_data["email"], "password": password
    }
    login_response = client.post(
        "/login",
        json=login_data
    )
    assert login_response.status_code == 200
    assert "Authorization" in login_response.cookies
    token_value = login_response.cookies["Authorization"]
    assert token_value is not None
    assert token_value.strip('"').startswith("Bearer")

    cookies = {"Authorization": token_value}
    yield cookies, user, user_data, password
