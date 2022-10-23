from datetime import datetime

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
    pass


class CharityProjectDB(CharityProjectBase):
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = datetime.now().isoformat(timespec='seconds')
    close_date: datetime = None

    # class Config:
    #     orm_mode = True