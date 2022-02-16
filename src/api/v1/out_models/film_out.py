from datetime import date
from typing import Optional

from api.v1.out_models.base_out import BaseOutModel


class FilmShortOut(BaseOutModel):
    title: str
    imdb_rating: Optional[float] = None


class FilmOut(BaseOutModel):
    title: str
    description: str = None
    type: str
    genres: Optional[list[dict[str, str]]] = None
    imdb_rating: Optional[float] = None
    creation_date: Optional[date] = None
    certificate: str = None
    age_limit: str = None
    directors: Optional[list[dict[str, str]]] = None
    actors: Optional[list[dict[str, str]]] = None
    writers: Optional[list[dict[str, str]]] = None
