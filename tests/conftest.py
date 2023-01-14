import os
import warnings
from asyncio import get_event_loop
from pathlib import Path

import databases
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from config.config import main_settings
from main import app
from config.db_config import MainMetaDB, engine
import pytest_asyncio
from alembic.config import Config
import alembic
from alembic import command
from config.db_config import database
import asyncio

settings = main_settings()

register_user_data: dict = {
    "phone": "79113559292",
    "email": "test.testmail@gmail.com",
    "password": "testpass123",
    "first_name": "Tester",
    "last_name": "Tester",
    "mid_name": "Tester"
}

register_user_without_posts_data: dict = {
    "phone": "79113219494",
    "email": "test.testmailwithout@gmail.com",
    "password": "testpass123",
    "first_name": "Tester2",
    "last_name": "Tester2",
    "mid_name": "Tester2"
}


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop


@pytest_asyncio.fixture()
async def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    async with engine.begin() as conn:
        await conn.run_sync(MainMetaDB.metadata.drop_all)
        await conn.run_sync(MainMetaDB.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def async_client(event_loop):
    lifespan = LifespanManager(app)
    httpx_client = AsyncClient(app=app, base_url="http://127.0.0.1:8000/")
    async with httpx_client as client, lifespan:
        yield client


@pytest_asyncio.fixture
async def login_user(async_client):
    payload = {"username": register_user_data['email'], "password": register_user_data["password"]}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    response = await async_client.post("/api/v1/authorization/login", headers=headers, data=payload)
    response_json = response.json()
    token: str = f"Bearer {response_json['access_token']}"
    return token


@pytest_asyncio.fixture
async def login_user_without_posts(async_client):
    payload = {"username": register_user_without_posts_data['email'],
               "password": register_user_without_posts_data["password"]}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    response = await async_client.post("/api/v1/authorization/login", headers=headers, data=payload)
    response_json = response.json()
    token: str = f"Bearer {response_json['access_token']}"
    return token
