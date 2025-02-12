from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

app = FastAPI()

class Reservation(BaseModel):
    name: str = Field(..., max_length=50)
    email: str
    date: datetime
    special_requests: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not value.endswith('@naver.com'):
            raise ValueError("naver.com만 됩니다")
        return value

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: datetime) -> datetime:
        if value <= datetime.now():
            raise ValueError("예약 날짜는 현재 시간보다 이후여야 합니다")
        return value

@app.post('/reservation/')
def reserv(res: Reservation):
    return {"reservation": res}