from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.out_models.film_out import FilmOut, FilmShortOut
from models.film import Film
from services.film_service import FilmService, get_film_service
from services.utils import get_nested_term_query, get_sort_body

router = APIRouter()


@router.get('/search',
            name='Поиск кинопроизведения',
            description='Полнотекстовый поиск по кинопроизведениям',
            response_model=list[FilmShortOut],
            response_model_exclude_unset=True)
async def search_films(query: str,
                       page_number: int = 0,
                       page_size: int = 20,
                       film_service: FilmService = Depends(
                           get_film_service)) -> list[FilmShortOut]:
    films: list[Film] = await film_service.search_films(
        query, page_number, page_size)
    return [FilmShortOut(id=film.id, title=film.title, imdb_rating=film.rating)
            for film in films]


@router.get('/{uuid}',
            name='Поиск кинопроизведения по uuid',
            description='Поиск кинопроизведения по его uuid',
            response_model=FilmOut,
            response_model_exclude_unset=True)
async def get_film_detail(uuid: str,
                          film_service: FilmService = Depends(get_film_service)
                          ) -> FilmOut:
    film: Film = await film_service.get_cached_object(uuid)
    return FilmOut(id=film.id,
                   title=film.title,
                   description=film.description,
                   type=film.type,
                   genres=film.genres,
                   imdb_rating=film.rating,
                   creation_date=film.creation_date,
                   age_limit=film.age_limit,
                   directors=film.directors,
                   actors=film.actors,
                   writers=film.writers)


@router.get('/{uuid}/similar',
            name='Поиск похожих произведений',
            description='''Поиск похожих кинопроизведений по uuid 
            данного кинопроизведения''',
            response_model=list[FilmShortOut],
            response_model_exclude_unset=True)
async def get_similar_films(uuid: str,
                            sort: str = '-imdb_rating',
                            page_number: int = 0,
                            page_size: int = 20,
                            film_service: FilmService = Depends(
                                get_film_service)
                            ) -> list[FilmShortOut]:
    body = get_sort_body(sort)
    films = await film_service.get_similar_films(
        uuid, page_number, page_size, body)
    return [FilmShortOut(id=film.id, title=film.title, imdb_rating=film.rating)
            for film in films]


@router.get('/',
            name='Список кинопроизведений',
            description='''Получение списка кинопроизведений с возможностью 
            фильтрации по жанру и сортировки по полю рейтинга''',
            response_model=list[FilmShortOut],
            response_model_exclude_unset=True)
async def get_films_list_sorted(sort: str = '-imdb_rating',
                                filter_genre: str = None,
                                page_number: int = 0,
                                page_size: int = 20,
                                film_service: FilmService = Depends(
                                    get_film_service)) -> list[FilmShortOut]:
    body = get_sort_body(sort)
    if filter_genre:
        body = body | get_nested_term_query('genres', filter_genre)
    films: list[Film] = await film_service.get_cached_object_list(
        page_number, page_size, body)
    return [FilmShortOut(id=film.id, title=film.title, imdb_rating=film.rating)
            for film in films]
