from typing import Optional

from fastapi import FastAPI

app = FastAPI()


# 쿼리 매개변수는 uri에 따로 적지 않음
@app.get('/items/')
def item(category: str = "all", page: Optional[int]=None) -> dict:
    if page is None:
        return {"category": category}
    return {"category": category, "page": page}
