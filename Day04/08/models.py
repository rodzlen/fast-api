from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from pydantic import BaseModel, field_serializer, field_validator, Field ,condecimal

class User(BaseModel):
    user_id : str
    username : str
    password : str
    email : str | None = None
    is_active : bool = 'No'

    @field_serializer('user_id')
    @classmethod
    def set_user_id(cls, value):
        value = str(uuid4())
        return value

    @field_validator('username')
    @classmethod
    def check_username(cls, value):
        if value == '' or None:
            raise ValueError('incorrect input username')
        return value

    @field_serializer('is_active')
    @classmethod
    def set_is_active(cls, value):
        if value:
            value = 'Yes'
            return value
        value = 'No'
        return value

class Order(BaseModel):
    order_id : int
    username : str
    total_price : condecimal(decimal_places=2)
    is_paid : bool = 'No'
    created_at : datetime  = Field(default_factory=datetime.utcnow)

    @field_validator('order_id')
    @classmethod
    def check_order_id(cls, value):
        if value =='' or not value:
            raise ValueError('incorrect order_id')
        return value

    @field_validator('username')
    @classmethod
    def check_username(cls, value):
        if value == '' or None:
            raise ValueError('incorrect input username')
        return value

    @field_serializer('is_paid')
    @classmethod
    def set_is_paid(cls, value):
        if value:
            value = 'Yes'
            return value
        value = 'No'
        return value
    @field_serializer('created_at')
    @classmethod
    def set_created_at(cls, value :datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')

class Product(BaseModel):
    product_id : str = Field(...)
    name : str = Field(...)
    price : float = Field(...)
    discount : float = 0
    final_price : float

    @field_serializer('final_price')
    @classmethod
    def set_final_price(cls, value, price, discount):
        value = price - (price - discount * 100)
