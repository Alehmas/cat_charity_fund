from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base


class Donation(Base):
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now())
    close_date = Column(DateTime, default=None)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Донат {self.id} с fully_invested= {self.fully_invested} и invested_amount={self.invested_amount}'
        )