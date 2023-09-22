from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services.google_api import (
    spreadsheets_create, set_user_permissions,
    spreadsheets_update_value
)

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""
    projects = await charity_project_crud.get_closed_projects(
        session
    )
    spreadsheet_id, report_url = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(spreadsheet_id,
                                        projects,
                                        wrapper_services)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return report_url
