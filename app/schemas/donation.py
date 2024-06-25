from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator

from app.constants import DONATION_ZERRO_ERROR


class DonationBaseDB(BaseModel):
    comment: Optional[str] = Field(None, title='Комментарий')
    full_amount: int = Field(..., title='Сумма')
    id: int = Field(..., title='Идентификатор')
    create_date: datetime = Field(..., title='Начало')


class DonationGetAllDB(DonationBaseDB):
    user_id: int = Field(..., title='Пользователь')
    invested_amount: int = Field(..., title='Пожертвование')
    fully_invested: bool = Field(..., title='Распределено')
    close_date: Optional[datetime] = Field(None, title='Завершено')

    class Config:
        orm_mode = True


class CreateDonation(BaseModel):
    full_amount: PositiveInt = Field(..., title='Сумма')
    comment: Optional[str] = Field(None, title='Комментарий')

    @validator('full_amount')
    def check_full_amount(cls, value):
        if value <= 0:
            raise ValueError(DONATION_ZERRO_ERROR)
        return value


class RetreiveDonation(DonationBaseDB):

    class Config:
        orm_mode = True
