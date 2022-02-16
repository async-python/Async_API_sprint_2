from datetime import date
from typing import Optional

from models.base_model import OrjsonBase


class FilmShort(OrjsonBase):
    title: str
    rating: Optional[float] = None


class Film(OrjsonBase):
    title: str
    description: Optional[str] = None
    type: str
    genres: Optional[list[dict[str, str]]] = None
    rating: Optional[float] = None
    creation_date: Optional[date] = None
    certificate: str = None
    age_limit: str = None
    file_path: str = None
    directors: Optional[list[dict[str, str]]] = None
    actors: Optional[list[dict[str, str]]] = None
    writers: Optional[list[dict[str, str]]] = None


class FilmId(OrjsonBase):
    pass
