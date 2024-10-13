from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.constants import DEFAULT_INVESTED_AMOUNT
from app.schemas.constants import (
    FULL_AMOUNT, FULLY_INVEST_EXAMPLE, ID_EXAMPLE,
    INVESTED_AMOUNT, MAX_LEN_NAME, MIN_LEN_NAME,
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        title='Название',
        min_length=MIN_LEN_NAME,
        max_length=MAX_LEN_NAME,
    )
    description: Optional[str] = Field(None, title='Описание')
    full_amount: Optional[PositiveInt] = Field(None, title='Требуемая сумма')

    class Config:
        title = 'Базовая схема проекта'


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        title = 'Схема проекта для обновления'
        orm_mode = True
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Нужны игрушки',
                'description': 'Для всех котиков мира',
                'full_amount': FULL_AMOUNT
            }
        }

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Название проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(
        ...,
        title='Название',
        min_length=MIN_LEN_NAME,
        max_length=MAX_LEN_NAME,
    )
    description: str = Field(..., title='Описание')
    full_amount: PositiveInt = Field(..., title='Требуемая сумма')

    class Config:
        title = 'Схема проекта для создания'
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int = Field(..., title='Порядковый номер')
    invested_amount: int = Field(
        DEFAULT_INVESTED_AMOUNT,
        title='Сколько пожертвовано',
    )
    fully_invested: bool = Field(False, title='Собрана нужная сумма')
    create_date: datetime = Field(..., title='Дата открытия проекта')
    close_date: Optional[datetime] = Field(None, title='Дата закрытия проекта')

    class Config:
        title = 'Схема проекта для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                'name': 'Песики - наше все',
                'description': 'очень хочу им помочь',
                'full_amoun': FULL_AMOUNT,
                'id': ID_EXAMPLE,
                'invested_amount': INVESTED_AMOUNT,
                'fully_invested': FULLY_INVEST_EXAMPLE,
                'create_date': '2023-07-22T02:18:40.662286'
            }
        }
