# Reference: https://tortoise.github.io/examples/fastapi.html#main-py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from app.settings import DB_CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI.

    This context manager makes sure to register the Tortoise ORM for the given
    FastAPI app and waits for the database to be fully connected before
    yielding control.

    If `app.state.testing` is set to `True`, the test database setup
    (`lifespan_test`) is used instead.

    This context manager is an async generator, so it should be used with an
    `async with` statement.
    """
    async with RegisterTortoise(app=app, config=DB_CONFIG, generate_schemas=False, add_exception_handlers=True):
        # db connected
        yield
        # app teardown
    # db connections closed
