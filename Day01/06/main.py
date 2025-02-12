from typing import Optional

from pydantic import BaseModel,Field
from fastapi import FastAPI

app = FastAPI()

class Product(BaseModel):
    name: str
    price : float = Field(..., gt=0)
    description : Optional[str] = "No desription"

@app.post('/products/')
def create_item(product:Product):
    if product.price < 0:
        return {"msg": "가격을 확인하세요"}
    return {"name":product.name, "price":product.price, "description" : product.description}