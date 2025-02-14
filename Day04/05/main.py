
from datetime import timedelta, datetime
import random
from fastapi import FastAPI
from pydantic import BaseModel, Field

class CreateOtp(BaseModel):
    phone_number : str
    otp : int = random.randint(100000,999999)
    otp_expiry : str = Field(default_factory=lambda : (datetime.utcnow()+timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"))

app =FastAPI()

@app.post('/')
def post(otp:CreateOtp):
    return otp