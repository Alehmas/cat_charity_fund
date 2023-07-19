from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Base class with a set of common methods for models."""

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Get all objects of the given class."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        """Create a new object of the given class."""
        if user is not None:
            obj_in['user_id'] = user.id
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
