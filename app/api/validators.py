from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject

PROJECT_NAME_MESSAGE = 'Проект с таким именем уже существует!'
PROJECT_NOT_EXIST_MESSAGE = 'Проекта не существует!'
ERR_PROJECT_CLOSED = 'В проект были внесены средства, не подлежит удалению!'
ERR_PROJECT_INVESTED = 'Закрытый проект нельзя редактировать!'
AMOUNT_MESSAGE = 'Сумма не может быть меньше внесенной!'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail=PROJECT_NAME_MESSAGE,
        )


async def check_full_amount(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail=PROJECT_NAME_MESSAGE,
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=PROJECT_NOT_EXIST_MESSAGE
        )
    return project


def check_project_can_deleted(
        project: CharityProject,
) -> None:
    if project.fully_invested is True or project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=ERR_PROJECT_CLOSED
        )


def check_project_open(
        project: CharityProject,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=ERR_PROJECT_INVESTED
        )


def check_summ(
        project: CharityProject,
        full_amount: int
) -> None:
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail=AMOUNT_MESSAGE
        )
