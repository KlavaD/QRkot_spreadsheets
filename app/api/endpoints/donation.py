from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationDB, DonationUserDB, DonationCreate
from app.services.invest import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получает список всех пожертвований.\n
    Только для суперюзеров.
    """
    donations = await donation_crud.get_multi(session)

    return donations


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Сделать пожертвование.\n
    """
    projects = await charity_project_crud.get_open(session)
    new_donation = await donation_crud.create(
        donation,
        session,
        False,
        user)
    projects = invest(new_donation, projects)
    session.add(new_donation)
    session.add_all(projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Получает список своих пожертвований.
    """
    donations = await donation_crud.get_user_donations(user.id, session)

    return donations
