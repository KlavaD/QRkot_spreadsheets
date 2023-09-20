from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_project_exists,
    check_project_can_deleted, check_project_open, check_summ
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (CharityProjectDB, CharityProjectCreate,
                                        CharityProjectUpdate)
from app.services.invest import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""

    projects = await charity_project_crud.get_multi(session)

    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Создает благотворительный проект.
    """

    await check_name_duplicate(project.name, session)
    donations = await donation_crud.get_open(session)
    new_project = await charity_project_crud.create(
        project,
        session,
        False,
    )
    donations = invest(new_project, donations)
    session.add(new_project)
    session.add_all(donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    Нельзя удалять закрытый проект.
    """

    project = await check_project_exists(project_id, session)
    check_project_can_deleted(project)
    await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),

):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """

    project = await check_project_exists(project_id, session)
    check_project_open(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_summ(project, obj_in.full_amount)

    project = await charity_project_crud.update(project, obj_in, session)
    return project
