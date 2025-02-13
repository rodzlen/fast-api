from typing import Optional

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel,Field, field_validator

app = FastAPI()

dummy_movies = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan", "release_year": 2010},
    {"id": 2, "title": "The Dark Knight", "director": "Christopher Nolan", "release_year": 2008},
    {"id": 3, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014},
    {"id": 4, "title": "Parasite", "director": "Bong Joon-ho", "release_year": 2019},
    {"id": 5, "title": "The Matrix", "director": "Lana Wachowski, Lilly Wachowski", "release_year": 1999},
    {"id": 6, "title": "Pulp Fiction", "director": "Quentin Tarantino", "release_year": 1994},
    {"id": 7, "title": "The Godfather", "director": "Francis Ford Coppola", "release_year": 1972},
    {"id": 8, "title": "Fight Club", "director": "David Fincher", "release_year": 1999},
    {"id": 9, "title": "Forrest Gump", "director": "Robert Zemeckis", "release_year": 1994},
    {"id": 10, "title": "The Shawshank Redemption", "director": "Frank Darabont", "release_year": 1994},
]

class Movie(BaseModel):
    id : int
    title : str = Field(..., max_length=30)
    director : str = Field(max_length=30)
    release_year : int

    @field_validator('id')
    @classmethod
    def validate_id(cls, value):
        if not value:
            raise ValueError('id값을 필수로 입력해야 합니다')
        for exist_id in [movie['id'] for movie in dummy_movies]:
            if value == exist_id:
                raise ValueError('이미 존재하는 id입니다.')
        return value

# 전체 영화 목록 조회
@app.get('/movies')
def get_movie_list():
    return dummy_movies



#title로 조회
@app.get('/movies/')
def get_movie_by_id(title:Optional[str]=None, movie_id:Optional[int]=None,director: Optional[str]=None, year:Optional[int]=None):
    for m in dummy_movies:
        if title == m['title']:
            return m
        if movie_id == m['id']:
            return m
        if director == m['director']:
            return m
        if year == m['release_year']:
            return m
    return HTTPException(status_code=404, detail='Not Found Data')

@app.post('/movies/')
def post_movie(movie:Movie):
    new_movie = dict(movie)
    dummy_movies.append(new_movie)
    return movie

@app.put('/movies/{movie_id}')
def put_movie(movie_id:int, movie:dict=Body(None)):
    new_movie = dict(movie)
    for m in dummy_movies:
        if m['id']==movie_id:
            m['title'] = new_movie['title']
            m['director'] = new_movie['director']
            m['release_year'] = new_movie['release_year']
            return {"update":m}

@app.delete('/movies/{movie_id}')
def delete_movie(movie_id:int):
    for index, m in enumerate(dummy_movies):
        if m['id'] == movie_id:
            dummy_movies.pop(index)
            return m
