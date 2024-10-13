from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import DEFAULT_INVESTED_AMOUNT
from app.schemas.constants import DONATE_EXAMPLE


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None, title='Комментарий')
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')

    class Config:
        title = 'Базовая схема пожертвования'


class DonationCreate(DonationBase):

    class Config:
        extra = Extra.forbid
        title = 'Схема пожертвования для создания'
        schema_extra = {
            'example': {
                'comment': 'От всей души',
                'full_amount': DONATE_EXAMPLE
            }
        }


class DonationDB(DonationBase):
    id: int = Field(..., title='ID пожертвования')
    create_date: datetime = Field(..., title='Дата внесения пожертвования')

    class Config:
        title = 'Схема пожертвования для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                'comment': 'От всей души',
                'full_amount': DONATE_EXAMPLE,
                'id': 2,
                'create_date': '2023-07-21T23:54:05.177Z'
            }
        }


class DonationDBSuper(DonationDB):
    user_id: Optional[int] = Field(None, title='ID пользователя')
    invested_amount: int = Field(
        DEFAULT_INVESTED_AMOUNT,
        title='Сколько вложено',
    )
    fully_invested: bool = Field(False, title='Вложена полная сумма')
    close_date: Optional[datetime] = Field(None, title='Дата вложения')

    class Config:
        title = 'Схема пожертвования для получения (advanced)'
        orm_mode = True
        schema_extra = {
            'example': {
                'comment': 'От всей души',
                'full_amount': DONATE_EXAMPLE,
                'id': 2,
                'create_date': '2023-07-21T23:54:05.177Z',
                'user_id': 1,
                'invested_amount': 200,
                'fully_invested': 0
            }
        }
