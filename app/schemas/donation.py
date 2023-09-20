from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field

from app.schemas.abstract import CommonFieldsSchemas


class DonationDB(CommonFieldsSchemas):
    id: int
    user_id: int
    comment: str

    class Config(CommonFieldsSchemas.Config):
        orm_mode = True


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(..., example='1200')
    comment: Optional[str]


class DonationUserDB(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]
    id: Optional[int]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True
