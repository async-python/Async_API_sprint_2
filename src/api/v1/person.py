from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.out_models.film_out import FilmShortOut
from api.v1.out_models.person_out import PersonOutFull, PersonOutShort
from models.film import Film
from models.person import Person
from services.person_service import PersonService, get_person_service
from services.utils import get_sort_body

router = APIRouter()


@router.get('/search',
            name='Поиск персоны',
            description='Полнотекстовый поиск по персонам',
            response_model=list[PersonOutShort],
            response_model_exclude_unset=True)
async def search_persons(query: str,
                         page_number: int = 0,
                         page_size: int = 20,
                         person_service: PersonService = Depends(
                             get_person_service)) -> list[PersonOutShort]:
    persons: Optional[list[Person]] = await person_service.search_persons(
        query, page_number, page_size)
    return [PersonOutShort(
        id=person.id,
        full_name=person.full_name,
        birth_date=person.birth_date) for person in persons]


@router.get('/{uuid}',
            name='Поиск персоны по uuid',
            description='Поиск персоны по uuid',
            response_model=PersonOutFull,
            response_model_exclude_unset=True)
async def get_person_detail(uuid: str,
                            person_service: PersonService = Depends(
                                get_person_service)
                            ) -> PersonOutFull:
    person: Optional[Person] = await person_service.get_cached_object(uuid)
    return PersonOutFull(id=person.id,
                         full_name=person.full_name,
                         birth_date=person.birth_date,
                         role=person.role,
                         film_ids=person.films)


@router.get('/{uuid}/film',
            name='Фильмы с участием персоны',
            description='''Список фильмов с участием uuid персоны, 
            доступна сортировка по рейтингу''',
            response_model=list[FilmShortOut],
            response_model_exclude_unset=True)
async def get_films_by_person(uuid: str,
                              sort: str = '-imdb_rating',
                              page_number: int = 0,
                              page_size: int = 20,
                              person_service: PersonService = Depends(
                                  get_person_service)
                              ) -> list[FilmShortOut]:
    body = get_sort_body(sort)
    films: Optional[list[Film]] = await person_service.get_person_films(
        uuid, page_number, page_size, body)
    return [FilmShortOut(id=film.id, title=film.title, imdb_rating=film.rating)
            for film in films]


@router.get('/',
            name='Список персон',
            description='Список всех доступных персон',
            response_model=list[PersonOutShort],
            response_model_exclude_unset=True)
async def get_persons_list(page_number: int = 0,
                           page_size: int = 20,
                           genre_service: PersonService = Depends(
                               get_person_service)
                           ) -> list[PersonOutShort]:
    persons: Optional[
        list[Person]] = await genre_service.get_cached_object_list(
        page_number, page_size)
    return [PersonOutShort(
        id=person.id,
        full_name=person.full_name,
        birth_date=person.birth_date) for person in persons]
