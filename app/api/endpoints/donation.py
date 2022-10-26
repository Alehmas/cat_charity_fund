from fastapi import APIRouter, Depends, HTTPException

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import create_donation_crud, get_all_donat_crud
from app.schemas import DonationCreate, DonationDB, DonationAllDB

router = APIRouter()


@router.post('/', response_model=DonationCreate,)
async def create_new_donation(
        donat: DonationCreate,
        session: AsyncSession = Depends(get_async_session),):
    new_donat = await create_donation_crud(donat, session)
    return new_donat


@router.get('/', response_model=List[DonationAllDB],)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),):
    all_donat = await get_all_donat_crud(session)
    return all_donat


@router.get('/me', response_model=List[DonationDB],)
async def read_all_my_donation(
        session: AsyncSession = Depends(get_async_session),):
    all_donat = await get_all_donat_crud(session)
    return all_donat