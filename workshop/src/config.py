from enum import Enum
from pydantic import BaseModel


# Class which describes a single measurement
class InputFeatures(BaseModel):
    danceability: float
    energy: float
    loudness: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float

    class Config:
        schema_extra = {
            "example": {
                "danceability": 0.802,
                "energy": 0.587,
                "loudness": -11.891,
                "speechiness": 0.067,
                "acousticness": 0.0116,
                "instrumentalness": 0.872,
                "liveness": 0.0863,
                "valence": 0.256,
                "tempo": 122.005,
            }
        }


class Term(str, Enum):
    short_term = "short_term"
    medium_term = "medium_term"
    long_term = "long_term"
