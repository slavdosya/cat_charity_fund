from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.constants import DEFAULT_INVESTED_AMOUNT


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        title='Название',
        min_length=1,
        max_length=100,
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
                'full_amount': 1000
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
        min_length=1,
        max_length=100,
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
                'full_amoun': 1500,
                'id': 19,
                'invested_amount': 360,
                'fully_invested': 0,
                'create_date': '2023-07-22T02:18:40.662286'
            }
        }
