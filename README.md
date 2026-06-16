# Nutshell

Nutshell - сервис сокращения ссылок с авторизацией пользователей. Проект состоит из backend API на FastAPI и отдельного 
(!Backend находится в активной разработке) frontend-приложения на React/Vite.

## Важно 

frontend-приложения на React/Vite. в данный момент существует как заглушка под будущие развитие проект
(!!На данный момент работа над frontend-приложением не ведется) 

## Стек

Backend:

- Python 3.12
- FastAPI
- SQLAlchemy AsyncIO
- asyncpg
- PostgreSQL
- Alembic
- PyJWT + bcrypt
- uv для управления зависимостями
- Ruff, MyPy, Bandit, pytest-asyncio в dev-зависимостях

Frontend:

- React 19
- Vite
- ESLint
- npm

Инфраструктура:

- Docker
- Docker Compose
- PostgreSQL 17.9
- pgAdmin 4

## Структура проекта

```text
.
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/             # API routers
│   │   ├── auth/            # JWT, password hashing, login logic
│   │   ├── database/        # async SQLAlchemy database provider
│   │   ├── links/           # link shortening domain
│   │   ├── users/           # users domain
│   │   └── alembic/         # database migrations
│   ├── prestartmigrations.sh
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/                # React/Vite frontend
├── docker-compose.yaml      # backend + PostgreSQL + pgAdmin
└── dockerfile               # backend image
```
### ps Марк если дочитал сюда не суди строго за качество readme писал два часа 

## API

Backend запускается на `http://localhost:8000`.

Основной префикс API: `/api/v1`.

Доступные группы эндпоинтов:

- `POST /api/v1/auth/register` - регистрация пользователя.
- `POST /api/v1/auth/login/` - получение JWT токена.
- `GET /api/v1/users/id/{user_id}` - получение пользователя по id.
- `GET /api/v1/users/by-email?email=...` - получение пользователя по email.
- `POST /api/v1/links/shorten` - создание короткой ссылки.
- `GET /api/v1/links/{slug}` - редирект slug.

Swagger UI доступен по адресу `http://localhost:8000/docs`.

## Переменные окружения

Backend использует настройки из `backend/src/config.py`. Переменные читаются с префиксом `NUTSHELL_CONFIG__`, вложенные поля разделяются через `__`.

Минимально необходимая переменная:

```env
NUTSHELL_CONFIG__DB__URL=postgresql+asyncpg://user:password@localhost:5432/nutshell_dev
```

Для Docker Compose уже задано:

```env
NUTSHELL_CONFIG__DB__URL=postgresql+asyncpg://user:password@pg:5432/nutshell_dev
```

JWT по умолчанию ожидает ключи:

```text
backend/certs/jwt-user-private.pem
backend/certs/jwt-user-public.pem
```

Сгенерировать их можно так:

```bash
mkdir -p backend/certs
openssl genrsa -out backend/certs/jwt-user-private.pem 2048
openssl rsa -in backend/certs/jwt-user-private.pem -pubout -out backend/certs/jwt-user-public.pem
```

Без этих файлов регистрация может работать, но логин и выпуск JWT токена упадут при чтении ключей.

## Локальный запуск backend

Требования:

- Python 3.12.13 или новее
- uv
- PostgreSQL

1. Поднять PostgreSQL:

```bash
docker compose up -d pg
```

2. Создать `backend/.env`:

```env
NUTSHELL_CONFIG__DB__URL=postgresql+asyncpg://user:password@localhost:5432/nutshell_dev
```

3. Установить зависимости:

```bash
uv sync --project backend
```

4. Сгенерировать JWT-ключи, если их еще нет:

```bash
mkdir -p backend/certs
openssl genrsa -out backend/certs/jwt-user-private.pem 2048
openssl rsa -in backend/certs/jwt-user-private.pem -pubout -out backend/certs/jwt-user-public.pem
```

5. Применить миграции:

```bash
uv run --project backend alembic -c backend/src/alembic.ini upgrade head
```

6. Запустить backend:

```bash
uv run --project backend uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

После запуска:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

## Локальный запуск frontend

Требования:

- Node.js
- npm

Команды:

```bash
cd frontend
npm install
npm run dev
```

По умолчанию Vite откроет frontend на `http://localhost:5173`.

Сейчас frontend находится в стартовом состоянии шаблона Vite/React и не подключен к backend API.

## Запуск через Docker

Docker Compose поднимает:

- `project` - backend API на порту `8000`.
- `pg` - PostgreSQL на порту `5432`.
- `pgadmin` - pgAdmin на порту `5050`.

Команда:

```bash
docker compose up --build
```

После запуска:

- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050`

Доступы pgAdmin:

```text
email: admin@admin.org
password: admin
```

Доступы PostgreSQL из Docker-сети:

```text
host: pg
port: 5432
database: nutshell_dev
user: user
password: password
http://127.0.0.1:5050```

Доступы PostgreSQL с хоста:

```text
host: localhost
port: 5432
database: nutshell_dev
user: user
password: password
```

При старте backend контейнер выполняет `backend/prestartmigrations.sh`, который применяет Alembic-миграции перед запуском Uvicorn.

## Основные нюансы проекта

- В Docker Compose frontend не запускается. Его нужно запускать отдельно через `npm run dev`.
- Backend зависит от PostgreSQL и переменной `NUTSHELL_CONFIG__DB__URL`.
- Для JWT нужны RSA-ключи в `backend/certs/` или переопределение путей через переменные `NUTSHELL_CONFIG__AUTH_JWT__PRIVATE_KEY_PATH` и `NUTSHELL_CONFIG__AUTH_JWT__PUBLIC_KEY_PATH`.
- В `docker-compose.yaml` у backend сервиса нет явного `depends_on` на PostgreSQL. Если backend стартует раньше базы и миграции падают, повторите запуск `docker compose up project` после готовности `pg`.
- Миграции лежат в `backend/src/alembic/versions`.
- Имя базы в compose сейчас `nutshell_dev` это тестовая база созданная в рамках docker под демо для backend управление базой доступно через pgadmin информация для подключения pgadmin находится выше
- Настройки backend можно хранить в `backend/.env`; файл читается автоматически через Pydantic Settings.

## Полезные команды

Проверка frontend:

```bash
cd frontend
npm run lint
npm run build
```

Проверка backend линтером:

```bash
uv run --project backend ruff check backend
```

Форматирование backend:

```bash
uv run --project backend ruff format backend
```
