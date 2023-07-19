from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """"Get a project from the database by name."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_charity_project_by_id(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        """"Get a project from the database by id."""
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        db_project = db_project.scalars().first()
        return db_project

    async def update_charity_project(
            self,
            db_project: CharityProject,
            project_in: CharityProjectUpdate,
            session: AsyncSession,
    ) -> CharityProject:
        """"Update the project in the database."""
        obj_data = jsonable_encoder(db_project)
        update_data = project_in.dict(exclude_unset=True)
        if 'full_amount' in update_data:
            if obj_data['invested_amount'] == update_data['full_amount']:
                update_data['fully_invested '] = True
        for field in obj_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def delete_charity_project(
            self,
            db_project: CharityProject,
            session: AsyncSession,
    ) -> CharityProject:
        """"Delete a project from the database."""
        await session.delete(db_project)
        await session.commit()
        return db_project


charity_project_crud = CRUDCharityProject(CharityProject)
