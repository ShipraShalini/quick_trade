import asyncio
from typing import Iterator

import pytest as pytest
import pytest_asyncio
from settings import DB_CONFIG
from starlette.testclient import TestClient
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise

from app.api import app


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest_asyncio.fixture(scope="module", autouse=True)
async def initialize_tests(request, event_loop):
    db_url = "sqlite://:memory:"

    config = generate_config(
        db_url,
        app_modules={"models": DB_CONFIG["apps"]["models"]["models"]},
        testing=True,
        connection_label="models",
    )

    async with RegisterTortoise(
        app=app,
        config=config,
        generate_schemas=True,
        _create_db=True,
    ):
        # db connected
        yield
        # app teardown
    # db connections closed
    await Tortoise._drop_databases()
