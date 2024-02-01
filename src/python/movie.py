"""Define classes with data structures based one the input csv file."""
from dataclasses import dataclass
from typing import Literal


@dataclass
class Movie:
    """Movie attributes found in the given movie csv."""

    movie_id: int
    title: str
    orig_movie_name: str | None
    year_movie: int
    list_genres_current_row: list[str]


@dataclass
class User:
    """User attributes found in the given user csv."""

    user_id: int
    gender: Literal["M", "F"]
    age: int
    cap: int
    job: str


@dataclass
class Rating:
    """User attributes found in the given user csv."""

    user_id: int
    movie_id: int
    rating: int
    timestamp: int
