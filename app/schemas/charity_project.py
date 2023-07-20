from datetime import datetime

from typing import Optional, Union
from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    """The base schema class for charitable projects."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Charity project creation scheme."""

    pass


class CharityProjectUpdate(CharityProjectCreate):
    """Charity project renewal scheme."""

    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1)
    full_amount: Optional[int] = Field(gt=0)

    @validator('name', 'description', 'full_amount')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('The field cannot be empty!')
        return value


class CharityProjectDB(CharityProjectCreate):
    """Scheme for obtaining charity project data from the database."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime

    class Config:
        orm_mode = True


class CharityProjectAll(CharityProjectDB):
    """Scheme for obtaining a list of charitable projects."""

    close_date: Union[datetime, None]
