from pydantic import BaseModel

class User(BaseModel):
    username : str
    password : str
    email : str | None = None
    phone : str | None = None
