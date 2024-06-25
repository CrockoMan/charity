from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models import CharityProject
from app.constants import (
    CHARITY_CLOSED, CHARITY_DESCRIPTION_INCORRECT, CHARITY_NAME_EXISTS,
    CHARITY_NAME_INCORRECT, CHARITY_NOT_FOUND, CHARITY_SUM_MIN_THEM_INVESTED,
    CHARITY_WAS_INVESTED
)


async def check_charity_duplicate(
    charity_name: str,
    session: AsyncSession,
) -> None:
    charity = await charity_crud.get_charity_by_name(charity_name, session)
    if charity is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_NAME_EXISTS,
        )


def check_charity_description(
    description: str,
) -> None:
    if description is None or description == '':
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=CHARITY_DESCRIPTION_INCORRECT,
        )


async def check_charity_name(
    name: str,
    session: AsyncSession
) -> None:
    if name is None or name == '':
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=CHARITY_NAME_INCORRECT,
        )
    charity = await charity_crud.get_charity_by_name(name, session)
    if charity is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_NAME_EXISTS,
        )


def check_charity_full_amount(
    full_amount: int,
    charity: CharityProject,
) -> None:
    if full_amount is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=CHARITY_NAME_INCORRECT,
        )
    if full_amount < charity.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_SUM_MIN_THEM_INVESTED,
        )


async def check_charity_exists(
    charity_id: int,
    session: AsyncSession,
):
    charity = await charity_crud.get(charity_id, session)
    if charity is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=CHARITY_NOT_FOUND
        )
    return charity


def check_charity_not_invested(
        charity: CharityProject,
) -> None:
    if charity.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_WAS_INVESTED
        )


async def charity_check_open(
        charity: CharityProject,
        session: AsyncSession,
):
    charity = await charity_crud.get_charity_by_name(charity.name, session)
    if charity.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_CLOSED,
        )
