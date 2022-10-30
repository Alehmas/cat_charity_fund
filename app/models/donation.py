from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, BaseCharityMixin


class Donation(BaseCharityMixin, Base):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
