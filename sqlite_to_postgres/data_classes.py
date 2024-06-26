from dataclasses import dataclass
import uuid
from datetime import datetime

@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str
    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True)
class Filmwork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True)  
class GenreFilmwork:
    id: uuid.UUID
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: datetime

@dataclass(frozen=True)   
class PersonFilmwork:
    id: uuid.UUID
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: datetime


TABLE_TO_DATACLASS = {
     'genre' : Genre,
     'person' : Person,
     'film_work' : Filmwork,
     'person_film_work' : PersonFilmwork,
     'genre_film_work' : GenreFilmwork,
}