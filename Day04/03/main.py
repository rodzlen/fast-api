from pydantic import BaseModel, computed_field
from fastapi import FastAPI
class Product(BaseModel):
    name : str
    price : float
    discount : float = 0


    @computed_field(return_type=float)
    @property
    def final_price(self):
        final_price = self.price - (self.price * self.discount*0.01)
        return round(final_price,1)

app = FastAPI()

@app.post('/price')
def calculate(product:Product):
    return product