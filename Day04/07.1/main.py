from datetime import datetime

from pydantic import BaseModel, field_serializer, Field
from fastapi import FastAPI
class User(BaseModel):
    username : str
    is_active : bool
    created_at : datetime = Field(default_factory=datetime.utcnow)

    class Config :
        json_encoders = {
            datetime : lambda v: v.strftime('%Y-%m-%d %H:%M:%S'),
            bool : lambda  v: 'Yes' if v else 'No'
        }
app = FastAPI()

@app.post('/')
def asd(user : User):
    print(user.model_dump_json())
    return user

test1 = User(username="test1", is_active=False)
test2 = User(username="test2", is_active=False)
print(test1.model_dump_json(exclude={'username'}))
print(test1)