# FastAPI Blank Project

Чистый проект FastAPI с современной архитектурой и готовой инфраструктурой.

## Особенности

- 🚀 **FastAPI** с асинхронной поддержкой
- 📚 **Scalar** документация API
- 🗄️ **SQLAlchemy 2.0** с async поддержкой
- 🔐 **JWT аутентификация** готова к использованию
- 📝 **Pydantic** для валидации данных
- 🛡️ **Middleware** для безопасности и логирования
- ⚙️ **Настройки** через переменные окружения
- 🏗️ **Чистая архитектура** с разделением слоев

## Структура проекта

```
blank_FastAPI/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Основное приложение
│   ├── core/                   # Ядро приложения
│   │   ├── config.py          # Настройки
│   │   ├── database.py        # Подключение к БД
│   │   ├── exceptions.py      # Обработка исключений
│   │   ├── logging.py         # Настройка логирования
│   │   └── middleware.py      # Middleware
│   ├── api/                   # API роуты
│   │   └── v1/
│   ├── models/                # SQLAlchemy модели
│   ├── schemas/               # Pydantic схемы
│   ├── services/              # Бизнес-логика
│   └── utils/                 # Утилиты
│       ├── dependencies.py    # FastAPI зависимости
│       └── security.py        # Безопасность и JWT
├── run.py                    # Скрипт запуска
├── requirements.txt          # Зависимости pip
├── pyproject.toml           # Poetry конфигурация
└── env.example              # Пример переменных окружения
```

## Быстрый старт

### 1. Клонирование и установка

```bash
# Клонирование репозитория
git clone <your-repo-url>
cd blank_FastAPI

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
# Копирование файла настроек
cp env.example .env

# Редактирование настроек
nano .env  # или любой другой редактор
```

### 3. Запуск приложения

```bash
# Запуск через скрипт
python run.py

# Или напрямую через uvicorn
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## API Документация

- **Scalar UI**: http://localhost:8000/scalar (в debug режиме)
- **Swagger UI**: http://localhost:8000/docs (в debug режиме)
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Доступные эндпоинты

- `GET /` - Главная страница
- `GET /health` - Проверка состояния приложения

## Настройки

Основные настройки задаются через переменные окружения в файле `.env`:

```env
# Основные настройки
APP_NAME=FastAPI App
DEBUG=false
VERSION=0.1.0

# Сервер
HOST=0.0.0.0
PORT=8000

# База данных
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname

# Безопасность
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Разработка

### Установка с Poetry

```bash
# Установка Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Установка зависимостей
poetry install

# Активация окружения
poetry shell

# Запуск
poetry run python run.py
```

### Линтеры и форматирование

```bash
# Форматирование кода
black app/
isort app/

# Проверка типов
mypy app/

# Линтер
flake8 app/
```

### Тестирование

```bash
# Запуск тестов
pytest

# С покрытием
pytest --cov=app
```

## База данных

### PostgreSQL (рекомендуется)

```bash
# Установка PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Создание базы данных
sudo -u postgres createdb your_db_name

# Настройка в .env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/your_db_name
```

### SQLite (для разработки)

```bash
# Настройка в .env
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

## Миграции (Alembic)

```bash
# Инициализация Alembic
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "Initial migration"

# Применение миграций
alembic upgrade head
```

## Архитектура

### Core модули

- **config.py** - Настройки приложения через Pydantic Settings
- **database.py** - Настройка SQLAlchemy и сессий
- **exceptions.py** - Кастомные исключения и обработчики
- **logging.py** - Настройка логирования
- **middleware.py** - HTTP middleware (CORS, логирование, безопасность)

### Utils модули

- **dependencies.py** - FastAPI зависимости (DB сессии, аутентификация)
- **security.py** - JWT токены, хеширование паролей

## Безопасность

Проект включает базовые меры безопасности:

- JWT аутентификация
- Хеширование паролей с bcrypt
- CORS настройки
- Заголовки безопасности
- Валидация входных данных

## Логирование

Настроено структурированное логирование:

- Консольный вывод
- Файловое логирование в `logs/app.log`
- Логирование запросов с уникальными ID
- Различные уровни для разработки и продакшена

## Производство

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run.py"]
```

### Переменные окружения для продакшена

```env
DEBUG=false
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/prod_db
CORS_ORIGINS=https://yourdomain.com
```

## Лицензия

MIT License

## Поддержка

Если возникли вопросы или проблемы, создайте issue в репозитории.
