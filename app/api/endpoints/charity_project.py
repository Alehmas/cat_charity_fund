from fastapi import APIRouter, Depends, HTTPException

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import (
    create_charity_project, get_project_id_by_name, read_all_project_db,
    update_charity_project, get_charity_project_by_id, delete_charity_project)
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate

router = APIRouter(prefix='/charity_project')


@router.post('/', response_model=CharityProjectDB,)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),):
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
)
async def partially_update_charity_project(
        # ID обновляемого объекта.
        project_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
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
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_charity_project_exists(
        project_id, session
    )
    project = await delete_charity_project(
        project, session
    )
    return project


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