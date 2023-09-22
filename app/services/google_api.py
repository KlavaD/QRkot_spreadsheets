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
BIG_DATA_ERROR = 'Данные не помещаются в созданную таблицу: {} больше {} {}'
CELL_RANGE = 'R1C1:R{row_end}C{col_end}'


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=SPREADSHEET_BODY,
) -> list[Union[str, Any]]:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = copy.deepcopy(spreadsheet_body)
    spreadsheet_body['properties']['title'] = f'Отчет от {now_date_time}'
    service = await wrapper_services.discover('sheets', 'v4')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    spreadsheet_url = response['spreadsheetUrl']
    return [
        spreadsheet_id,
        spreadsheet_url
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
    row_in_table = len(table_values)
    column_in_table = max(map(len, table_values))
    if row_in_table > ROW_COUNT:
        raise ValueError(
            BIG_DATA_ERROR.format(row_in_table, ROW_COUNT, 'строк')
        )
    if column_in_table > COLUMN_COUNT:
        raise ValueError(
            BIG_DATA_ERROR.format(column_in_table, COLUMN_COUNT, 'столбцов')
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=CELL_RANGE.format(
                row_end=row_in_table,
                col_end=column_in_table
            ),
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
