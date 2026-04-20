from fastapi import APIRouter, HTTPException, Depends
from models import Movie, MoviePatch, MovieCreate
from sqlmodel import select, Session
from database import get_session
from typing import Union

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/")
def get_movies(director: Union[str, None] = None, session: Session = Depends(get_session)):
    if director:
        movies = session.exec(select(Movie).where(Movie.director == director)).all()
    else:
        movies = session.exec(select(Movie)).all()
    return movies


@router.get("/{movie_id}")
def get_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.post("/", status_code=201)
def new_movie(movie_data: MovieCreate, session: Session = Depends(get_session)):
    movie = Movie.model_validate(movie_data)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.put("/{movie_id}")
def update_movie(movie_id: int, movie_data: MovieCreate, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie_dict = movie_data.model_dump()
    for key, value in movie_dict.items():
        setattr(movie, key, value)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    session.delete(movie)
    session.commit()
    return {"message": "Movie deleted"}


@router.patch("/{movie_id}")
def partial_update(movie_id: int, movie_data: MoviePatch, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie_dict = movie_data.model_dump(exclude_unset=True)
    for key, value in movie_dict.items():
        setattr(movie, key, value)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie
