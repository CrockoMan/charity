from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.charity_project import CharityDB

FORMAT = "%Y/%m/%d %H:%M:%S"

MAX_ROW = 1000
MAX_COL = 10

HEADER = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

SPREADSHEET_TITLE = 'Отчет от {}'
SPREADSHEET_BODY = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=MAX_ROW,
            columnCount=MAX_COL,
        )
    ))]
)


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body: dict = SPREADSHEET_BODY
) -> dict:
    spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
        datetime.now().strftime(FORMAT)
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return dict(
        spreadsheet_id=response['spreadsheetId'],
        spreadsheet_url=response['spreadsheetUrl'],
    )


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity: list[CharityDB],
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_header = deepcopy(HEADER)
    table_header[0][1] = datetime.now().strftime(FORMAT)
    table_body = [
        *table_header,
        *[list(map(str, [
            item.name, item.close_date - item.create_date, item.description
        ])) for item in charity],
    ]

    row = len(table_body)
    col = max(map(len, table_body))
    if row > MAX_ROW or col > MAX_COL:
        raise ValueError(
            'Выход за размер документа.'
            f'Максимум строк {MAX_ROW} сформировано {row}'
            f'Мксимум столбцов {MAX_COL} сформировано {col}'
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_body
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{len(table_body)}C{max(map(len, table_body))}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
