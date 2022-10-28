from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud import get_charity_project_by_id, get_project_id_by_name
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_name_dublicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await get_charity_project_by_id(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_full(
        project_id: int,
        session: AsyncSession,
):
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    db_project = db_project.scalars().first()
    if db_project.fully_invested == 1:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_charity_project_full_del(
        project: CharityProject,
        session: AsyncSession,
):
    if project.fully_invested == 1:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )

async def check_invested_sum(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
):
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    db_project = db_project.scalars().first()
    if obj_in.full_amount and db_project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=400,
            detail='Желаемая сумма пожертвований не может быть меньше внесенной!'
        )