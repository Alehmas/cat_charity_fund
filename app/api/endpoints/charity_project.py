from fastapi import APIRouter, Depends, HTTPException

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charity_project_exists, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import (
    create_charity_project, read_all_project_db,
    update_charity_project, delete_charity_project)
from app.schemas import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate

router = APIRouter()


@router.post(
    '/', response_model=CharityProjectDB, dependencies=[Depends(current_superuser)],)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await create_charity_project(project, session)
    return new_project


@router.get('/', response_model=List[CharityProjectDB],)
async def get_all_project(
        session: AsyncSession = Depends(get_async_session),):
    all_project = await read_all_project_db(session)
    return all_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        # ID обновляемого объекта.
        project_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    # Получаем объект из БД по ID.
    # В ответ ожидается либо None, либо объект класса MeetingRoom.
    project = await check_charity_project_exists(project_id, session)
    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)
    # Передаём в корутину все необходимые для обновления данные.
    project = await update_charity_project(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id, session
    )
    project = await delete_charity_project(
        project, session
    )
    return project
