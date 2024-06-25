from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    charity_check_open, check_charity_description, check_charity_duplicate,
    check_charity_exists, check_charity_full_amount, check_charity_name,
    check_charity_not_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.services.distribution import donate_distribution
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityCreate, CharityDB, CharityUpdate, CharityUpdateResponse
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    charity = await charity_crud.get_multi(session)
    return charity


@router.post(
    '/',
    response_model=CharityDB,
    dependencies=(Depends(current_superuser),)
)
async def create_charity_project(
    charity: CharityCreate,
    session: AsyncSession = Depends(get_async_session),
):
    check_charity_description(charity.description)
    await check_charity_name(charity.name, session)
    await check_charity_duplicate(charity.name, session)
    charity = await charity_crud.create(charity, session, commit=False)
    donations = await donation_crud.get_undistributed(session)

    if len(donations) != 0:
        distributions = donate_distribution(charity, donations)
        session.add_all(distributions)

    await session.commit()
    await session.refresh(charity)

    return charity


@router.delete(
    '/{charity_id}',
    response_model=CharityDB,
    dependencies=(Depends(current_superuser),)
)
async def delete_charity_project(
    charity_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity = await check_charity_exists(charity_id, session)
    check_charity_not_invested(charity)
    charity = await charity_crud.remove(charity, session)
    return charity


@router.patch(
    '/{charity_id}',
    response_model=CharityUpdateResponse,
    dependencies=(Depends(current_superuser),)
)
async def update_charity_project(
    charity_id: int,
    charity_update: CharityUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity = await check_charity_exists(charity_id, session)
    await charity_check_open(charity, session)

    if charity_update.description is not None:
        check_charity_description(charity_update.description)
    if charity_update.name is not None:
        await check_charity_name(charity_update.name, session)
    if charity_update.full_amount:
        check_charity_full_amount(charity_update.full_amount, charity)

    if (
            charity_update.description or
            charity_update.name or
            charity_update.full_amount
    ):
        charity = await charity_crud.update(charity, charity_update, session)

        return charity
