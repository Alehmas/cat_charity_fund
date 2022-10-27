from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject, Donation


# Функция работает с асинхронной сессией, 
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def add_free_donate(
        session: AsyncSession,
) -> None:
    all_donate = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False
        )
    )
    for donat in all_donate:
        ## остановился здесь!!!!!
    await session.commit()


