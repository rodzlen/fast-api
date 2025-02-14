import re
from typing import Optional

from pydantic import BaseModel, field_validator
from fastapi import FastAPI

class UserRegister(BaseModel):
    username : str
    password : str
    confirm_password : Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        has_upper = bool(re.search(r"[A-Z]", value))  # 대문자 포함 여부
        has_digit = bool(re.search(r"\d", value))  # 숫자 포함 여부
        has_special = bool(re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>,.?/~`\\|-]", value))
        # 8자 이상, 최소 1개 이상의 대문자, 숫자, 특수문자
        if len(value) < 8:
            raise ValueError('비밀번호는 8자 이상 되어야 합니다')
        if  has_digit and has_special and has_upper:
            return value
        raise ValueError('최소 1개 이상의 대문자, 숫자, 특수문자를 포함해야 합니다')

app = FastAPI()

@app.post('/check')
def get_valid(user:UserRegister):
    return user