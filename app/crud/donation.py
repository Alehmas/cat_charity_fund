from typing import List

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation, User
from app.schemas import DonationCreate


async def create_donation_crud(
        new_donat: DonationCreate,
        session: AsyncSession,
        user: User
) -> Donation:
    if user is not None:
        new_donat['user_id'] = user.id
    db_donat = Donation(**new_donat)
    session.add(db_donat)
    await session.commit()
    await session.refresh(db_donat)
    return db_donat


async def get_all_donat_crud(
        session: AsyncSession,
) -> List[Donation]:
    db_donats = await session.execute(select(Donation))
    return db_donats.scalars().all()


async def get_donats_by_user(
        session: AsyncSession, user: User
) -> List[Donation]:
    # Получаем объект класса Result.
    db_donats = await session.execute(
        # Получить все объекты Reservation.
        select(Donation).where(
            # Где внешний ключ meetingroom_id 
            # равен id запрашиваемой переговорки.
            Donation.user_id == user.id
        )
    )
    return db_donats.scalars().all()





