from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator
from pydantic.types import conint

from app.constants import (
    CHARITY_EMPTY_DESCRIPTION, CHARITY_EMPTY_NAME, NAME_MAX_LEN
)


class CharityBase(BaseModel):
    name: str = Field(
        ...,
        title='Название',
        max_length=NAME_MAX_LEN,
        nullable=False
    )
    description: str = Field(..., title='Описание', nullable=False)
    full_amount: int = Field(..., title='Сумма к сбору', gt=0)

    @validator('name')
    def check_name(cls, value):
        if value is None or len(value.strip()) == 0:
            raise ValueError(CHARITY_EMPTY_NAME)
        return value

    @validator('description')
    def check_description(cls, value):
        if value is None or len(value.strip()) == 0:
            raise ValueError(CHARITY_EMPTY_DESCRIPTION)
        return value


class CharityDB(CharityBase):
    id: int
    invested_amount: int = Field(title='Пожертвование')
    fully_invested: bool = Field(False, title='Сумма собрана')
    create_date: datetime = Field(title='Дата начала')
    close_date: Optional[datetime] = Field(None, title='Дата окончания')

    class Config:
        orm_mode = True


class CharityCreate(CharityBase):
    pass


class CharityUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=NAME_MAX_LEN,
        title='Название',
    )
    description: Optional[str] = Field(None, title='Описание')
    full_amount: Optional[conint(gt=0)] = Field(None, title='Сумма к сбору')

    class Config:
        extra = Extra.forbid


class CharityUpdateResponse(CharityUpdate, CharityDB):

    class Config:
        orm_mode = True
