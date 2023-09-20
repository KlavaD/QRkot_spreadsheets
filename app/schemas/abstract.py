from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, NonNegativeInt, Field, BaseModel, Extra


class CommonFieldsSchemas(BaseModel):
    full_amount: Optional[PositiveInt] = Field(0, example='1200')
    invested_amount: Optional[NonNegativeInt] = Field(0)
    fully_invested: Optional[bool] = Field(False)
    create_date: Optional[datetime]
    close_date: Optional[datetime] = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1
