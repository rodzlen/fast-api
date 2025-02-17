from fastapi import FastAPI, Depends
from database import get_db, Product
from sqlalchemy.orm import Session
from pydantic import BaseModel

class ProductRequests(BaseModel):
    name : str
    price : int
app = FastAPI()

@app.get('/products')
def get_products(db : Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
@app.get('/products/{product_id}')
def get_product(product_id:int, db : Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    return product

@app.post('/products')
def post_product(request: ProductRequests, db:Session= Depends(get_db)):
    new_product = Product(name=request.name, price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product