from typing import Optional

from models.base_model import OrjsonBase


class Genre(OrjsonBase):
    name: str
    description: Optional[str] = None
