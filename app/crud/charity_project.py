from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectUpdate


# Функция работает с асинхронной сессией, 
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession,
) -> CharityProject:
    # Конвертируем объект MeetingRoomCreate в словарь.
    #new_project_data = new_project.dict()
    
    # Создаём объект модели MeetingRoom.
    # В параметры передаём пары "ключ=значение", для этого распаковываем словарь.
    db_project = CharityProject(**new_project)
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


async def get_charity_project_by_id(
        project_id: int,
        session: AsyncSession,
) -> Optional[CharityProject]:
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    db_project = db_project.scalars().first()
    return db_project


async def update_charity_project(
        # Объект из БД для обновления.
        db_project: CharityProject,
        # Объект из запроса.
        project_in: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    # Представляем объект из БД в виде словаря.
    obj_data = jsonable_encoder(db_project)
    # Конвертируем объект с данными из запроса в словарь, 
    # исключаем неустановленные пользователем поля.
    update_data = project_in.dict(exclude_unset=True)
    # Перебираем все ключи словаря, сформированного из БД-объекта.
    if 'full_amount' in update_data:
        if obj_data['invested_amount'] == update_data['full_amount']:
            update_data['fully_invested '] = True
    for field in obj_data:
        # Если конкретное поле есть в словаре с данными из запроса, то...
        if field in update_data:
            # ...устанавливаем объекту БД новое значение атрибута.
            setattr(db_project, field, update_data[field])
    session.add(db_project)
    await session.commit()
    # Обновляем объект из БД.
    await session.refresh(db_project)
    return db_project


async def delete_charity_project(
        db_project: CharityProject,
        session: AsyncSession,
) -> CharityProject:
    await session.delete(db_project)
    await session.commit()
    return db_project