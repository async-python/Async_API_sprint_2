import asyncio
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from functional.settings import ConfTest
from multidict import CIMultiDictProxy

SERVICE_URL = 'http://127.0.0.1:8000'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(
        hosts=f'{ConfTest.elastic_host}:{ConfTest.elastic_port}')
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    client = await aioredis.Redis(
        host=ConfTest.redis_host, port=ConfTest.redis_port,
        password=ConfTest.redis_password)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
def make_get_request(session: aiohttp.ClientSession):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
