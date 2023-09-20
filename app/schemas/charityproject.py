from typing import Optional

from pydantic import Field, PositiveInt, BaseModel, Extra

from app.schemas.abstract import CommonFieldsSchemas

PROJECT_NAME_ERROR = 'Имя не может быть пустым'


class ProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(0, example='1200')

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectDB(CommonFieldsSchemas):
    id: int
    name: str = Field(None, max_length=100)
    description: str = Field(None)

    class Config(CommonFieldsSchemas.Config):
        orm_mode = True
        min_anystr_length = 1


class CharityProjectCreate(ProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt = Field(..., example='1200')


class CharityProjectUpdate(ProjectBase):
    pass
