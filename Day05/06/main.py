from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, Item
app = FastAPI()

class ItemCreate(BaseModel):
    name : str
    price : int

@app.post('/items/')
async def create_item(item: ItemCreate, db : Session = Depends(get_db)):
    if item.price <= 0:
        raise HTTPException(status_code=400, detail="0보다 큰 숫자를 입력")

    new_item = Item(name=item.name, price=item.price)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.get('/itemss/{item_id}')
async def get_item(item_id:int , db:Session = Depends(get_db)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=400, detail='Not found item')
    return item

