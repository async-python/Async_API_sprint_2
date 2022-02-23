import json
from http import HTTPStatus
from typing import Any

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException
from pydantic.json import pydantic_encoder
from pydantic.main import BaseModel
from pydantic.tools import parse_raw_as

from services.utils import get_pagination_query

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class TemplateService:

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch,
                 model: Any, es_index: str):
        self.redis = redis
        self.elastic = elastic
        self.model = model
        self.es_index = es_index

    async def get_cached_object(self, uuid: str):
        obj = await self._get_obj_from_cache(uuid)
        if not obj:
            obj = await self._get_obj_from_elastic(uuid)
            if not obj:
                return None
            await self._put_obj_to_cache(obj)

        return obj

    async def get_cached_object_list(self, page_number: int, page_size: int,
                                     query: dict = None):
        return await self._get_search_list_cached(
            page_number, page_size, query)

    async def _get_search_list_cached(self, page_number: int,
                                      page_size: int,
                                      query: dict = None,
                                      es_index: str = None,
                                      model: Any = None):
        key = f'{self.es_index}-{query}-{page_number}-{page_size}'
        obj_list = await self._get_list_from_cache(key, model)
        if not obj_list:
            obj_list = await self._get_list_from_elastic(
                page_number, page_size, query, es_index, model)
            if not obj_list:
                return None
            await self._put_list_to_cache(key, obj_list)
        return obj_list

    async def _get_list_from_elastic(
            self, page_number: int, page_size: int,
            query: dict = None, es_index=None, model=None):
        if not es_index:
            es_index = self.es_index
        if not model:
            model = self.model
        body = get_pagination_query(page_number, page_size)
        try:
            if query:
                body = body | query
            docs = await self.elastic.search(
                index=es_index,
                body=body
            )
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f'bad request')
        if not docs['hits']['total']['value']:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail='not found')
        return [model(**doc['_source']) for doc in
                docs['hits']['hits']]

    async def _get_obj_from_elastic(self, obj_id: str):
        result = await self.elastic.exists(index=self.es_index, id=obj_id)
        if result:
            doc = await self.elastic.get(index=self.es_index, id=obj_id)
            return self.model(**doc['_source'])
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='not found')

    async def _get_obj_from_cache(self, obj_id: str):
        data = await self.redis.get(obj_id)
        if not data:
            return None
        obj = self.model.parse_raw(data)
        return obj

    async def _get_list_from_cache(self, key: str, model: BaseModel = None):
        if not model:
            model = self.model
        data = await self.redis.get(key)
        if not data:
            return None
        return parse_raw_as(list[model], data)

    async def _put_obj_to_cache(self, obj: BaseModel):
        await self.redis.set(obj.id, obj.json(),  # noqa
                             ex=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_list_to_cache(self, key: str, objects: list[BaseModel]):
        list_json = json.dumps(objects, default=pydantic_encoder)
        await self.redis.set(key, list_json, ex=FILM_CACHE_EXPIRE_IN_SECONDS)
