import copy
from datetime import datetime
from operator import itemgetter
from typing import Union, Any

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 11
SPREADSHEET_BODY = dict(
    properties=dict(
        title='',
        locale='ru_RU'
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT
        )
    ))]
)
HEADER = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Названия проекта', 'Время сбора', 'Описание']
]
DATA_ERROR = 'Данные не помещаются в созданную таблицу'
START_CELLS = 'R1C1:'


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=copy.deepcopy(SPREADSHEET_BODY),
) -> list[Union[str, Any]]:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body['properties']['title'] = f'Отчет от {now_date_time}'
    service = await wrapper_services.discover('sheets', 'v4')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return [
        spreadsheet_id,
        'https://docs.google.com/spreadsheets/d/' + spreadsheet_id
    ]


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    header = copy.deepcopy(HEADER)
    header[0][1] = now_date_time
    projects = sorted(
        (
            (
                obj['name'],
                obj['close_date'] - obj['create_date'],
                obj['description']
            ) for obj in projects
        ),
        key=itemgetter(1)
    )
    table_values = [
        *header,
        *[list(map(str, project)) for project in projects],
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    stop_cells = (f'R{len(table_values)}'
                  f'C{max(len(column) for column in table_values)}')
    if len(table_values) > ROW_COUNT:
        raise ValueError(DATA_ERROR)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=START_CELLS + stop_cells,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
