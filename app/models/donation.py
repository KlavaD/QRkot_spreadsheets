from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.abstract import CommonFieldsModel


class Donation(CommonFieldsModel):
    user_id = Column(Integer(), ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (f'Дотация создана пользователем {self.user_id},'
                f'Комментарий: {self.comment}' + super.__repr__())
