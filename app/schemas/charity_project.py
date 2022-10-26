from datetime import datetime

from typing import Optional, Union
from pydantic import BaseModel, Extra, Field, validator


# Базовый класс схемы, от которого наследуем все остальные.
class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(1, gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1)
    full_amount: Optional[int] = Field(gt=0)

    @validator('name', 'description', 'full_amount')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Поле не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Union[datetime, None]

    class Config:
        orm_mode = True