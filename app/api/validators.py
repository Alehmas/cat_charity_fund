from http import HTTPStatus
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_name_dublicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности имени проекта"""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка наличия проекта в базе по ID"""
    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_full(
        project: CharityProject,
) -> None:
    """Проверка закрыт ли проект(собрана ли требуемая сумма)"""
    if project.fully_invested == 1:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_charity_project_full_del(
        project: CharityProject,
) -> None:
    """Проверка закрыт ли проект или внесены ли в него средства"""
    if project.fully_invested == 1 or project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_invested_sum(
        project: CharityProject,
        obj_in: CharityProjectUpdate,
) -> None:
    """Требуемая сумма должна быть больше внесеной"""
    if obj_in.full_amount and project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма должна быть больше внесеной!'
        )
