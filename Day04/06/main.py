from typing import Union, Optional

from pydantic import BaseModel, field_validator
from fastapi import FastAPI

app = FastAPI()

class AS(BaseModel):
    username : str
    phone : str
    score : Union[int , float]

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        if value =='' or None:
            value= "No num"
            return value

@app.post('/')
def azxc(code:AS):
    return code