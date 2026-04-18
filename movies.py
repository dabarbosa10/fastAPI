from fastapi import FastAPI, HTTPException

movies = [
    {"id": 1, "title": "Titanic", "director": "James Cameron", "year": 1997},
    {"id": 2, "title": "The Matrix", "director": "The Wachowskis", "year": 1999},
    {"id": 3, "title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008},
    {"id": 4, "title": "The Lord of the Rings: The Return of the King", "director": "Peter Jackson", "year": 2003}
]


app = FastAPI(title="Movies API")


@app.get("/")
def root():
    return {"message": "Welcome to the Movies API. Go to /movies to see all movies."}


@app.get("/movies")
def get_movies():
    return movies


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"message": "Movie not found"}


@app.post("/movies")
def new_movie(title: str, director: str, year: int):
    movies.append({"id": max(movie["id"] for movie in movies) + 1 if movies else 1, "title": title, "director": director, "year": year})
    return {"message": "Movie created"}


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, title: str, director: str, year: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movie["title"] = title
            movie["director"] = director
            movie["year"] = year
            return {"message": "Movie updated!"}
    return {"message": "Movie not found"}


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return {"message": "Movie deleted!"}
    raise HTTPException(status_code=404, detail="Movie not found")