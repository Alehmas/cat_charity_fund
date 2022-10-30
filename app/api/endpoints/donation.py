from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import Donation, CharityProject, User
from app.schemas import DonationAllDB, DonationCreate, DonationDB
from app.services.services import add_donate_to_project


router = APIRouter()


@router.post('/', response_model=DonationDB, response_model_exclude_none=True,)
async def create_new_donation(
        donat: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),) -> Donation:
    """Сделать пожертвование."""
    new_donat = await add_donate_to_project(
        new=donat, upgrade_model=CharityProject, session=session)
    new_donat = await donation_crud.create(new_donat, session, user)
    return new_donat


@router.get(
    '/',
    response_model=List[DonationAllDB],
    dependencies=[Depends(current_superuser)],)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session)
) -> List[Donation]:
    """Только для суперюзеров. Получает список всех пожертвований."""
    all_donat = await donation_crud.get_multi(session)
    return all_donat


@router.get(
    '/my', response_model=List[DonationDB], response_model_exclude={'user_id'})
async def read_all_my_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)) -> List[Donation]:
    """Получить список моих пожертвований."""
    all_donat = await donation_crud.get_donats_by_user(
        session=session, user=user)
    return all_donat
