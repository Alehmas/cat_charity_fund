from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donats_by_user(
            self, session: AsyncSession, user: User
    ) -> List[Donation]:
        """"Get all donations from individual users."""
        db_donats = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_donats.scalars().all()


donation_crud = CRUDDonation(Donation)
