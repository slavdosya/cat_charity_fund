from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import DuplicateException
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBSuper
from app.api.utils import funds_distribution, get_uninvested_objects

router = APIRouter()


@router.post('/', response_model=DonationDB, response_model_exclude_none=True)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    open_projects = await get_uninvested_objects(CharityProject, session)
    try:
        funds_distribution(opened_items=open_projects, funds=new_donation)
        await session.commit()
        await session.refresh(new_donation)
    except IntegrityError:
        await session.rollback()
        raise DuplicateException('Средства уже распределены')
    return new_donation


@router.get(
    '/',
    response_model=Optional[List[DonationDBSuper]],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=Optional[List[DonationDB]],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_by_user(user=user, session=session)
