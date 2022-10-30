from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_full,
                                check_charity_project_full_del,
                                check_invested_sum, check_name_dublicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models import Donation, CharityProject
from app.schemas import (CharityProjectAll, CharityProjectCreate,
                         CharityProjectUpdate)
from app.services.services import add_donate_to_project


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectAll,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров.
    Создает благотворительный проект."""
    await check_name_dublicate(project.name, session)
    new_project = await add_donate_to_project(
        new=project, upgrade_model=Donation, session=session)
    new_project = await charity_project_crud.create(new_project, session)
    return new_project


@router.get(
    '/', response_model=List[CharityProjectAll],
    response_model_exclude_none=True,)
async def get_all_project(
        session: AsyncSession = Depends(get_async_session),
) -> List[CharityProject]:
    """Получает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectAll,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров. Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной."""
    project = await check_charity_project_exists(project_id, session)
    await check_charity_project_full(project)
    await check_name_dublicate(obj_in.name, session)
    await check_invested_sum(project, obj_in)
    project = await charity_project_crud.update_charity_project(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectAll,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров.Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть."""
    project = await check_charity_project_exists(project_id, session)
    await check_charity_project_full_del(project)
    project = await charity_project_crud.delete_charity_project(
        project, session)
    return project
