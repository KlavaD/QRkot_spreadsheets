from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):

    async def get_user_donations(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        return db_obj.scalars().all()


donation_crud = CRUDDonation(Donation)
