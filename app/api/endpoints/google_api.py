from http import HTTPStatus
from typing import Optional

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    # response_model=list[CharityDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

) -> Optional[str]:
    """Только для суперюзеров."""
    projects = await charity_crud.get_projects_by_completion_rate(session)
    try:
        spreadsheet = await spreadsheets_create(wrapper_services)
        await set_user_permissions(
            spreadsheet.get('spreadsheet_id'),
            wrapper_services
        )
        await spreadsheets_update_value(
            spreadsheet.get('spreadsheet_id'),
            projects,
            wrapper_services
        )
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )

    return spreadsheet.get('spreadsheet_url')
