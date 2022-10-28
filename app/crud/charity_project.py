from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectUpdate


async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession,
) -> CharityProject:
    """"Функция создания проекта в БД"""
    db_project = CharityProject(**new_project)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(
        project_name: str,
        session: AsyncSession,
) -> Optional[int]:
    """"Функция получения проекта из БД по имени"""
    db_project_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == project_name
        )
    )
    db_project_id = db_project_id.scalars().first()
    return db_project_id


async def read_all_project_db(
        session: AsyncSession,
) -> List[CharityProject]:
    """"Функция получения всех проектов из БД"""
    db_project_id = await session.execute(select(CharityProject))
    return db_project_id.scalars().all()


async def get_charity_project_by_id(
        project_id: int,
        session: AsyncSession,
) -> Optional[CharityProject]:
    """"Функция получения проекта из БД по id"""
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    db_project = db_project.scalars().first()
    return db_project


async def update_charity_project(
        db_project: CharityProject,
        project_in: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    """"Функция обновления проекта в БД"""
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
        db_project: CharityProject,
        session: AsyncSession,
) -> CharityProject:
    """"Функция удаления проекта из БД"""
    await session.delete(db_project)
    await session.commit()
    return db_project
