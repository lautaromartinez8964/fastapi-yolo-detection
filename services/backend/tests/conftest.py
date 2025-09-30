# 测试文件的配置文件
# 包括Pytest连接到轻量数据库SQLite的配置，以及用户数据库表的内容

import os
import uuid

import pytest_asyncio
from tortoise import Tortoise


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    """
    Initialize Tortoise ORM once per test session using an in-memory SQLite database.
    This avoids touching the real database and keeps tests isolated and fast.
    """
    os.environ["TZ"] = "UFC"
    db_url = "sqlite://:memory:"

    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["src.database.models"]},
    )

    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture()
async def user_factory():
    from src.database.models import Users

    async def create_user(**kwargs):
        data = {
            "username": kwargs.get("username", f"u_{uuid.uuid4().hex[:8]}"),
            "full_name": kwargs.get("full_name", "Test User"),
            "password": kwargs.get("password", "pass1234"),
        }
        return await Users.create(**data)

    return create_user
