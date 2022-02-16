from typing import Optional

from api.v1.out_models.base_out import BaseOutModel


class GenreOut(BaseOutModel):
    name: str
    description: Optional[str] = None
