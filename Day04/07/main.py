from uuid import UUID, uuid4

from pydantic import BaseModel, field_serializer
from fastapi import FastAPI
class User(BaseModel):
    username : str
    is_active : bool

    @field_serializer('is_active')
    @classmethod
    def trans_is_active(cls, value):
        if value:
            return "Yes"
        return "No"

app = FastAPI()

@app.post('/')
def asd(user : User):
    print(user.model_dump_json())
    return user