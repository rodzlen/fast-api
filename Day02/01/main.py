from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field
# 엔드포인트 3개 모든책, 특정 책, search
#
books_db = [
    {"id":1, "title":"1984", "author": "George Orwell", "year": 1949},
    {"id":2, "title":"To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id":3, "title":"Brave New World", "author": "Aldous Huxley", "year": 1932},
]

app = FastAPI()

class Books(BaseModel):
    id : int
    title : str = Field(..., max_length=100)
    author : str = Field(..., max_length=50)
    year : int = Field(..., gt=1900, le=2025)

@app.get('/books/')
def book_list():
    return {"books":books_db}

@app.get('/books/search')
def get_book_by_keyword(author:str = ''):
    result = [book for book in books_db if book['author']== author]
    if not result:
        raise ValueError('결과가 없습니다')
    return {"books": result}

@app.get('/books/{book_id}')
def get_book_by_id(book_id: int ):
    for book in books_db:
        if book['id'] == book_id:
            return {"book":book}
        raise ValueError('없는 Id입니다.')


