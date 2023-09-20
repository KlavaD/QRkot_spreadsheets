from sqlalchemy import Column, Text, String

from app.models.abstract import CommonFieldsModel


class CharityProject(CommonFieldsModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'Проект {self.name}, {self.description}' + super.__repr__()
