from decimal import Decimal

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class OrderCreateRequest(BaseModel):
    user_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0)


class PaymentCreateRequest(BaseModel):
    amount: Decimal = Field(gt=0)
