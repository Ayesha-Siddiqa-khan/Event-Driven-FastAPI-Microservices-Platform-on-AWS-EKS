from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import OrderStatus


class OrderCreate(BaseModel):
    user_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    status: OrderStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
