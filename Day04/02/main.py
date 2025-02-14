from typing import Any

from pydantic import BaseModel, field_validator, model_validator
from fastapi import FastAPI


class ContactInfo(BaseModel):
    email : str | None = None
    phone_number : str | None  = None

    @model_validator(mode='before') # dict형태로 반환
    def validate_info(self):
        if not self['phone_number'] and not self['email']:
            raise ValueError('at least one phone nuber or email')
        return self



    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if value == '':
            value = None
            return value
        if not '@' in value or not '.' in value.split('@')[-1]:
            raise ValueError('incorrect email')
        return value

app = FastAPI()

@app.post('/check')
def check_info(user:ContactInfo):
    return user