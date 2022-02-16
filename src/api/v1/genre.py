from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.out_models.genre_out import GenreOut
from models.genre import Genre
from services.genre_service import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}',
            name='Поиск жанра',
            description='Поиск жанра по его uuid',
            response_model=GenreOut,
            response_model_exclude_unset=True)
async def get_genre_detail(genre_id: str,
                           genre_service: GenreService = Depends(
                               get_genre_service)
                           ) -> GenreOut:
    genre: Optional[Genre] = await genre_service.get_cached_object(genre_id)
    return GenreOut(id=genre.id,
                    name=genre.name,
                    description=genre.description)


@router.get('/',
            name='Список жанров',
            description='Список всех жанров',
            response_model=list[GenreOut],
            response_model_exclude_unset=True)
async def get_genres_list(page_number: int = 0,
                          page_size: int = 500,
                          genre_service: GenreService = Depends(
                              get_genre_service)
                          ) -> list[GenreOut]:
    genres: Optional[list[Genre]] = await genre_service.get_cached_object_list(
        page_number, page_size)
    return [GenreOut(
        id=genre.id,
        name=genre.name,
        description=genre.description) for genre in genres]
