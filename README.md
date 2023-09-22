# Проект Благотворительного фонда помощи котикам
В данном проекте реализована возможность создавать различные проекты и собирать дотации от желающих помочь. 
Автор - 
*   [Клавдия Дунаева](https://www.t.me/klodunaeva)


**Инструменты и стек:**- 
* Python 3.9+, 
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [FastAPI-Users](https://fastapi-users.github.io/fastapi-users/10.0/)
* [GoogleSheetsAPI](https://developers.google.cn/identity/protocols/oauth2/scopes#sheets)
* [GoogleDriveAPI](https://developers.google.com/drive/api/reference/rest/v3#Files)



**Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KlavaD/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Обновить pip:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать файл .env

```
APP_TITLE=
APP_DESCRIPTION=
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=
```
Добавить в него данные сервисного аккаунта Google
```
DATABASE_URL=
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```
А так же свою личную электронную почту ...@gmail.com
```
EMAIL= 
```
Выполните миграции

```
alembic upgrade head
```
Запустить FastAPI-сервер:
```
uvicorn main:app
```
[Посмотреть документацию и выполнить тестовые запросы](http://127.0.0.1:8000/docs)

[Посмотреть документацию ReDoc](http://127.0.0.1:8000/redoc)
