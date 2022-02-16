from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmId
from models.person import Person
from services.template_service import TemplateService
from services.utils import get_base_match_query, get_films_by_person_query

ROLES_MAP = {
    'actors': 'actor',
    'writers': 'writer',
    'directors': 'director'
}


class PersonService(TemplateService):
    film_index = 'movie'
    film_model = Film
    film_id_model = FilmId

    async def search_persons(
            self, request, page_number, page_size) -> list[Person]:
        search_field = 'full_name'
        query = get_base_match_query(search_field, request)
        persons: list[Person] = await self.get_cached_object_list(
            page_number, page_size, query)
        return persons

    async def get_person_films(
            self, uuid: str, page_number: int,
            page_size: int, query: dict = None) -> list[Film]:
        body = get_films_by_person_query(uuid)
        if query:
            body = body | query
        films: list[Film] = await self._get_search_list_cached(
            page_number, page_size, body, self.film_index, self.film_model)
        return films


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(
            get_elastic), ) -> PersonService:
    return PersonService(redis, elastic, Person, 'person')
