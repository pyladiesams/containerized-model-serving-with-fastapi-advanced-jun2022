from enum import Enum
from pydantic import BaseModel


class Term(str, Enum):
    short_term = "short_term"
    medium_term = "medium_term"
    long_term = "long_term"


class Song(BaseModel):
    name: str
    artists: str

    class Config:
        schema_extra = {
            "example": {
                "name": "De Diepte",
                "artists": "S10",
            }
        }


class PredOut(BaseModel):
    pass
