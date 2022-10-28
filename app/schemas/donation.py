from datetime import datetime

from typing import Optional, Union
from pydantic import BaseModel, Extra, Field


class DonationCreate(BaseModel):
    comment: Optional[str] = Field(None, min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationDB(DonationCreate):
    id: int
    create_date: datetime


class DonationAllDB(DonationDB):
    fully_invested: bool
    invested_amount: int
    user_id: Optional[int]