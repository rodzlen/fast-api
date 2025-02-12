from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    quantity: int = Field(..., gt=1)


class Order(BaseModel):
    id: int
    items: List[Item]
    total_price: float = Field(..., gt=0)


@app.post('/orders/')
def orders( order: Order):
    return {
        "id": order.id,
        "items": order.items,
        "total_price": order.total_price
    }
