from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union

movies = [
    {"id": 1, "title": "Titanic", "director": "James Cameron", "year": 1997},
    {"id": 2, "title": "The Matrix", "director": "The Wachowskis", "year": 1999},
    {"id": 3, "title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008},
    {"id": 4, "title": "The Lord of the Rings: The Return of the King", "director": "Peter Jackson", "year": 2003},
    {"id": 5, "title": "Inception", "director": "Christopher Nolan", "year": 2010}
]


app = FastAPI(title="Movies API")


class Movie(BaseModel):
    title: str
    director: str
    year: int
    genre: Union[str, None] = None


class MovieResponse(Movie):
    id: int


@app.get("/")
def root():
    return {"message": "Welcome to the Movies API. Go to /movies to see all movies."}


@app.get("/movies")
def get_movies(director: Union[str, None] = None):
    if director is None:
        return movies
    elif director:
        filtered = []
        for movie in movies:
            if movie["director"] == director:
                filtered.append(movie)
        return filtered


@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


@app.post("/movies")
def new_movie(movie_data: Movie):
    movies.append({"id": max(movie["id"] for movie in movies) + 1 if movies else 1,
                   "title": movie_data.title,
                   "director": movie_data.director,
                   "year": movie_data.year,
                   "genre": movie_data.genre})
    return {"message": "Movie created"}


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie_data: Movie):
    for movie in movies:
        if movie["id"] == movie_id:
            movie["title"] = movie_data.title
            movie["director"] = movie_data.director
            movie["year"] = movie_data.year
            movie["genre"] = movie_data.genre
            return {"message": "Movie updated!"}
    raise HTTPException(status_code=404, detail="Movie not found")


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return {"message": "Movie deleted!"}
    raise HTTPException(status_code=404, detail="Movie not found")

