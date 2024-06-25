# backend Благотворительного фонда
Фонд собирает пожертвования на различные целевые проекты, формирует отчёты о сборе средств в Google Sheets
##### Стек: Pyton, FastAPI, SQLAlchemy

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:CrockoMan/charity.git
```

```
cd charity
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:
* Если у вас Linux/macOS

    ```
    python3 -m pip install --upgrade pip
    ```
* Если у вас windows
* 
    ```
    pip install -r requirements.txt
    ```

Заполнить файл конфигурации .env
```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET
# Google API
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

Выполнить миграции

```
alembic upgrade head
```

Запсустить сервис:

```
uvicorn main:app --reload
```

### API сервиса доступен после запуска:  http://127.0.0.1:8000/docs/

Автор: [К.Гурашкин](https://github.com/CrockoMan)