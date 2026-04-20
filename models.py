from sqlmodel import SQLModel, Field
from pydantic import field_validator
from typing import Union


class MovieBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    director: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1888, le=2030)
    genre: Union[str, None] = Field(default=None, min_length=3)

    @field_validator("title")
    @classmethod
    def title_val(cls, v):
        if not v.strip():
            raise ValueError("This cannot be just blank spacces")
        return v.strip()

    @field_validator("director")
    @classmethod
    def director_capitalize(cls, v):
        return v.title()


class Movie(MovieBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)


class MovieCreate(MovieBase):
    pass


class MoviePatch(SQLModel):
    title: Union[str, None] = None
    director: Union[str, None] = None
    year: Union[int, None] = None
    genre: Union[str, None] = None
