import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import film, genre, person
from core import config
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.Redis(
        host=config.REDIS_HOST, port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD)
    elastic.es = AsyncElasticsearch(
        hosts=f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}')


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(film.router, prefix='/api/v1/film', tags=['Film'])
app.include_router(genre.router, prefix='/api/v1/genre', tags=['Genre'])
app.include_router(person.router, prefix='/api/v1/person', tags=['Person'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
