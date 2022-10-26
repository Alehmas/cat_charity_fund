from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_charity_project_by_id, get_project_id_by_name
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует',
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
