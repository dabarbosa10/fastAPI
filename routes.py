from fastapi import APIRouter, HTTPException
from models import Movie, MovieResponse, MoviePatch
from data import movies

router = APIRouter(prefix="/movies", tags=["Movies"])


def find_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


@router.get("/")
def get_movies():
    return movies


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    return find_movie(movie_id)


@router.post("/", status_code=201, response_model=MovieResponse)
def new_movie(movie_data: Movie):
    new_id = max(movie["id"] for movie in movies) + 1 if movies else 1
    movie_dict = movie_data.model_dump()
    movie_dict["id"] = new_id
    movies.append(movie_dict)
    return movie_dict


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie_data: Movie):
    movie = find_movie(movie_id=movie_id)
    movie.update(movie_data.model_dump())
    return movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id=movie_id)
    movies.remove(movie)
    return {"message": "Movie deleted!"}


@router.patch("/{movie_id}", response_model=MovieResponse)
def partial_update(movie_id: int, movie_data: MoviePatch):
    movie = find_movie(movie_id=movie_id)
    updates = movie_data.model_dump(exclude_unset=True)
    movie.update(updates)
    return movie
