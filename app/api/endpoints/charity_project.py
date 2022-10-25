from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import create_charity_project, get_project_id_by_name, read_all_project_db
from app.schemas import CharityProjectCreate, CharityProjectDB

router = APIRouter(prefix='/charity_project')


@router.post('/', response_model=CharityProjectDB,)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),):
    project_id = await get_project_id_by_name(project.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует',
        )
    new_project = await create_charity_project(project, session)
    return new_project

@router.get('/', response_model=list[CharityProjectDB],)
async def get_all_project(
        session: AsyncSession = Depends(get_async_session),):
    all_project = await read_all_project_db(session)
    return all_project