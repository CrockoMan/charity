from typing import List, Optional

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        charity = await session.execute(
            select(CharityProject).filter(
                CharityProject.name == name,
            )
        )
        return charity.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        charity = await session.execute(
            select(CharityProject).filter(
                CharityProject.fully_invested == 1
            ).order_by(
                desc(CharityProject.close_date - CharityProject.create_date)
            )
        )
        charity = charity.scalars().all()
        return charity


charity_crud = CRUDCharityProject(CharityProject)
