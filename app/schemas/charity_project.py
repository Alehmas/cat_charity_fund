from datetime import datetime

from typing import Optional, Union
from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1)
    full_amount: Optional[int] = Field(gt=0)

    @validator('name', 'description', 'full_amount')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('The field cannot be empty!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime

    class Config:
        orm_mode = True


class CharityProjectAll(CharityProjectDB):
    close_date: Union[datetime, None]
