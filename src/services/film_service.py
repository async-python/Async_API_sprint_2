from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.template_service import TemplateService
from services.utils import get_base_multimatch_query, get_nested_term_query


class FilmService(TemplateService):
    async def search_films(self, request: str,
                           page_number: int, page_size: int
                           ) -> Optional[list[Film]]:
        search_fields = ['title', 'description']
        query = get_base_multimatch_query(search_fields, request)
        films = await self.get_cached_object_list(page_number,
                                                  page_size, query)
        return films

    async def get_similar_films(self, uuid: str,
                                page_number: int,
                                page_size: int,
                                query: dict = None
                                ) -> Optional[list[Film]]:
        film: Film = await self.get_cached_object(uuid)
        if not film or not film.genres:
            return None
        field_name = 'genres'
        genres = [genre['id'] for genre in film.genres]
        body = get_nested_term_query(field_name, genres)
        if query:
            body = body | query
        films = await self.get_cached_object_list(page_number,
                                                  page_size, body)
        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(
            get_elastic), ) -> FilmService:
    return FilmService(redis, elastic, Film, 'movie')
