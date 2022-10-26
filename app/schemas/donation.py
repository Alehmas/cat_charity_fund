from datetime import datetime

from typing import Optional, Union
from pydantic import BaseModel, Extra, Field


class DonationCreate(BaseModel):
    comment: Optional[str] = Field(None, min_length=1)
    full_amount: int = Field(1, gt=0)

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationDB(DonationCreate):
    id: int
    invested_amount: int
    create_date: datetime


class DonationAllDB(DonationDB):
    fully_invested: bool
    close_date: Union[datetime, None]
    # user_id