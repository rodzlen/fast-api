import uuid
from datetime import datetime
from pydantic import BaseModel, field_validator, Field
from fastapi import FastAPI

class User(BaseModel):
    user_id : str = Field(default_factory= lambda : str(uuid.uuid4()))
    name : str
    role : str
    create_at : str = Field(default_factory= lambda :datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

a= User(name="asd", role='admin')
print(a)

app =FastAPI()

@app.post('/')
def post(user : User):
    return user