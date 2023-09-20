from datetime import datetime

from sqlalchemy import (
    Column, Integer, DateTime, Boolean, CheckConstraint, and_, text
)

from app.core.db import Base


class CommonFieldsModel(Base):
    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    __table_args__ = (
        CheckConstraint(
            and_(
                text('full_amount > 0'),
                text('invested_amount <= full_amount')
            )
        ),
    )

    def __repr__(self):
        return (
            f'Полная сумма {self.full_amount},'
            f'инвестировано {self.invested_amount}'
            f'Проект создан {self.create_date}'
            f'Проект закрыт {self.fully_invested}'
            f'Дата закрытия {self.close_date}'
        )
