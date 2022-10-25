from typing import Optional, List

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject
from app.schemas import CharityProjectCreate


# Функция работает с асинхронной сессией, 
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession,
) -> CharityProject:
    # Конвертируем объект MeetingRoomCreate в словарь.
    new_project_data = new_project.dict()
    
    # Создаём объект модели MeetingRoom.
    # В параметры передаём пары "ключ=значение", для этого распаковываем словарь.
    db_project = CharityProject(**new_project_data)
    session.add(db_project)

    # Записываем изменения непосредственно в БД. 
    # Так как сессия асинхронная, используем ключевое слово await.
    await session.commit()

    # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
    await session.refresh(db_project)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_project


async def get_project_id_by_name(
        project_name: str,
        session: AsyncSession,
) -> Optional[int]:
    # Получаем объект класса Result.
    db_project_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == project_name
        )
    )
    # Извлекаем из него конкретное значение.
    db_project_id = db_project_id.scalars().first()
    return db_project_id


async def read_all_project_db(
        session: AsyncSession,
) -> List[CharityProject]:
    # Получаем объект класса Result.
    db_project_id = await session.execute(select(CharityProject))
    return db_project_id.scalars().all()