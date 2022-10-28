from fastapi import APIRouter, Depends

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import create_donation_crud, get_all_donat_crud, get_donats_by_user
from app.models import User
from app.schemas import DonationCreate, DonationDB, DonationAllDB
from app.services.services import add_donate_to_project

router = APIRouter()


@router.post('/', response_model=DonationDB, response_model_exclude_none=True,)
async def create_new_donation(
        donat: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),):
    new_donat = await add_donate_to_project(donat, session)
    new_donat = await create_donation_crud(new_donat, session, user)
    return new_donat


@router.get(
    '/',
    response_model=List[DonationAllDB],
    dependencies=[Depends(current_superuser)],)
async def get_all_donation(session: AsyncSession = Depends(get_async_session),):
    """Только для суперюзеров."""
    all_donat = await get_all_donat_crud(session)
    return all_donat


@router.get(
    '/my', response_model=List[DonationDB], response_model_exclude={'user_id'})
async def read_all_my_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    """Получает список пожертвований для текущего пользователя."""
    all_donat = await get_donats_by_user(session=session, user=user)
    return all_donat