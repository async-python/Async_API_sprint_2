from datetime import date
from typing import Optional

from api.v1.out_models.base_out import BaseOutModel


class PersonOutShort(BaseOutModel):
    full_name: str
    birth_date: Optional[date] = None


class PersonOutFull(BaseOutModel):
    full_name: str
    birth_date: Optional[date] = None
    role: Optional[list[str]] = None
    film_ids: Optional[list[str]] = None
