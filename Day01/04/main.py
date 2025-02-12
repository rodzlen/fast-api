from typing import List, Optional
from fastapi import FastAPI,Query

app = FastAPI()

@app.get('/items/{order_id}/')
def get_user(order_id: int, items: Optional[List[str]] = Query(None) )-> dict:
    print(items)
    if not items:
        return {"order_id": order_id}
    return {"order_id": order_id, "items": {"item":item for item in items}}