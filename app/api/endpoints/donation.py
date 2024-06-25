from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_crud
from app.services.distribution import donate_distribution
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    CreateDonation, DonationGetAllDB, RetreiveDonation
)

router = APIRouter()


@router.get(
    '/',
    response_model=Optional[list[DonationGetAllDB]],
    dependencies=(Depends(current_superuser),),
    response_model_exclude_none=True,
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
):
    await donation_crud.get_multi(session)
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=RetreiveDonation,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: CreateDonation,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_crud.create(donation, session, user, False)
    charity = await charity_crud.get_undistributed(session)
    if len(charity) != 0:
        distributions = donate_distribution(donation, charity)
        session.add_all(distributions)

    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model=list[RetreiveDonation],
)
async def get_my_donation(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await donation_crud.get_by_user(user, session)
    return await donation_crud.get_by_user(user, session)
