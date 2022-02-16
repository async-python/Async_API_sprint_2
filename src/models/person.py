from datetime import date
from typing import Optional

from models.base_model import OrjsonBase


class Person(OrjsonBase):
    full_name: str
    birth_date: Optional[date] = None
    role: Optional[list[str]] = None
    films: Optional[list[str]] = None
