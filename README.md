# FastAPI Blank Project

Полноценный blank проект на FastAPI с использованием ООП подхода.

## Структура проекта

```
FastAPI_Blank_Project/
├── App/
│   ├── Core/                    # Ядро приложения
│   │   ├── Config.py           # Конфигурация
│   │   ├── Database.py         # Подключение к БД
│   │   └── Logger.py           # Логирование
│   ├── Models/                  # Модели БД (SQLAlchemy)
│   │   └── User.py             # Пример модели
│   ├── Schemas/                 # Pydantic схемы
│   │   └── User.py             # Пример схемы
│   ├── Services/                # Бизнес-логика
│   │   ├── UserService.py      # Пример сервиса
│   │   └── Dependencies.py     # DI зависимости
│   ├── Api/                     # API контроллеры
│   │   └── V1/                 # API версии 1
│   │       ├── Router.py       # Главный роутер V1
│   │       ├── UserController.py   # Пример контроллера
│   │       └── HealthController.py # Health check
│   ├── Scheduler/               # Планировщик задач
│   │   ├── SchedulerManager.py # Менеджер планировщика
│   │   ├── TaskRegistry.py     # Регистрация задач
│   │   └── Tasks/              # Задачи
│   │       └── ExampleTask.py  # Пример задачи
│   └── Main.py                  # Главный файл приложения
├── alembic/                     # Миграции БД
│   ├── versions/               # Версии миграций
│   └── env.py                  # Конфигурация Alembic
├── Scripts/                     # Скрипты утилит
│   ├── CreateMigration.py      # Создание миграции
│   └── ApplyMigrations.py      # Применение миграций
├── logs/                        # Логи (создается автоматически)
├── Run.py                       # Файл запуска
├── requirements.txt             # Зависимости
├── alembic.ini                 # Конфигурация Alembic
├── .env                        # Переменные окружения
├── example.env                 # Пример .env файла
└── .gitignore                  # Git ignore

```

## Возможности

- ✅ **FastAPI** - современный веб-фреймворк
- ✅ **SQLAlchemy 2.0** - async ORM для работы с PostgreSQL
- ✅ **Alembic** - миграции базы данных
- ✅ **APScheduler** - планировщик задач
- ✅ **Pydantic Settings** - валидация конфигурации
- ✅ **Structured Logging** - продвинутое логирование
- ✅ **CORS** - настроенный middleware
- ✅ **Dependency Injection** - для сервисов
- ✅ **ООП архитектура** - чистый и масштабируемый код
- ✅ **API Versioning** - версионирование API (v1)
- ✅ **Scalar** - современная документация API

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Скопируйте `example.env` в `.env` и настройте параметры:
```bash
cp example.env .env
```

5. Настройте подключение к PostgreSQL в `.env`:
```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_username
DATABASE_PASSWORD=your_password
```

## Миграции базы данных

### Создание миграции:
```bash
alembic revision --autogenerate -m "Описание миграции"
```

### Применение миграций:
```bash
alembic upgrade head
```

### Откат миграции:
```bash
alembic downgrade -1
```

### История миграций:
```bash
alembic history
```

### Текущая версия:
```bash
alembic current
```

## Запуск приложения

### Стандартный запуск (параметры из .env):
```bash
python Run.py
```

### С переопределением параметров:
```bash
python Run.py --host 0.0.0.0 --port 8080
```

### С автоперезагрузкой (для разработки):
```bash
python Run.py --reload
```

### С несколькими workers:
```bash
python Run.py --workers 4
```

### Все параметры:
```bash
python Run.py --help
```

## API Endpoints

После запуска доступны:

- **Scalar Docs**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/api/v1/health/
- **Users API**: http://localhost:8000/api/v1/users/

### Структура API

Все эндпоинты версионированы:
- `/api/v1/` - версия 1 API
- Для будущих версий можно создать `/api/v2/` и т.д.

## Планировщик задач

Планировщик задач встроен в приложение и запускается автоматически.

### Добавление новой задачи:

1. Создайте файл в `App/Scheduler/Tasks/YourTask.py`:
```python
from App.Core.Logger import get_logger

logger = get_logger(__name__)

async def your_task():
    logger.info("Выполнение вашей задачи")
    # Ваша логика здесь
```

2. Зарегистрируйте в `App/Scheduler/TaskRegistry.py`:
```python
from App.Scheduler.Tasks.YourTask import your_task

def register_all_tasks():
    scheduler_manager.add_job(
        func=your_task,
        trigger='interval',
        id='your_task_id',
        name='Ваша задача',
        minutes=10  # каждые 10 минут
    )
```

### Типы триггеров:

- **interval** - с интервалом (seconds, minutes, hours, days)
- **cron** - по расписанию (hour, minute, day_of_week, etc)
- **date** - одноразовое выполнение

## Разработка

### Добавление нового эндпоинта:

1. Создайте модель в `App/Models/`
2. Создайте схему в `App/Schemas/`
3. Создайте сервис в `App/Services/`
4. Создайте контроллер в `App/Api/V1/`
5. Зарегистрируйте роутер в `App/Api/V1/Router.py`

### Добавление новой версии API:

1. Создайте директорию `App/Api/V2/`
2. Создайте контроллеры в новой версии
3. Создайте `Router.py` для новой версии
4. Зарегистрируйте в `App/Main.py`

### Логирование:

```python
from App.Core.Logger import get_logger

logger = get_logger(__name__)

logger.debug("Отладочное сообщение")
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")
logger.critical("Критическая ошибка")
```

## Конфигурация

Все настройки находятся в `.env` файле и управляются через `App/Core/Config.py`.

Доступные настройки:
- Application (название, версия, debug режим)
- Server (host, port)
- Database (host, port, name, username, password, echo)
- CORS (origins, credentials, methods, headers)
- Logging (уровень, файл, размер, количество бэкапов)
- Scheduler (включен/выключен, timezone)

### Использование скриптов:

Создание миграции:
```bash
python Scripts/CreateMigration.py "Описание миграции"
```

Применение миграций:
```bash
python Scripts/ApplyMigrations.py
```

## Лицензия

MIT

