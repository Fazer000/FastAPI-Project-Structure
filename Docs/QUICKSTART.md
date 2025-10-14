# Быстрый старт

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Настройка окружения

Скопируйте `example.env` в `.env` и настройте параметры БД:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi_db
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
```

## 3. Создание и применение миграций

```bash
# Создать миграцию
alembic revision --autogenerate -m "Initial migration"

# Или используя скрипт
python Scripts/CreateMigration.py "Initial migration"

# Применить миграции
alembic upgrade head

# Или используя скрипт
python Scripts/ApplyMigrations.py
```

## 4. Запуск приложения

```bash
# Обычный запуск
python Run.py

# С автоперезагрузкой (для разработки)
python Run.py --reload

# С кастомным хостом и портом
python Run.py --host 0.0.0.0 --port 8080
```

## 5. Доступ к документации

После запуска откройте браузер:

- **Scalar API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health/

## Структура проекта

### Core (Ядро)
- `Config.py` - Конфигурация из .env
- `Database.py` - Async PostgreSQL подключение
- `Logger.py` - Настроенное логирование

### Models
- SQLAlchemy модели БД

### Schemas
- Pydantic схемы для валидации

### Services
- Бизнес-логика с dependency injection

### Api/V1
- Версионированные API контроллеры
- `Router.py` - Главный роутер версии

### Scheduler
- `SchedulerManager.py` - Управление APScheduler
- `TaskRegistry.py` - Регистрация задач
- `Tasks/` - Сами задачи планировщика

## Основные команды

```bash
# Создать миграцию
python Scripts/CreateMigration.py "Описание"

# Применить миграции
python Scripts/ApplyMigrations.py

# Запуск с reload
python Run.py --reload

# Запуск с несколькими workers
python Run.py --workers 4
```

## Добавление нового функционала

1. **Новая модель**:
   - Создать `App/Models/YourModel.py`
   - Импортировать в `alembic/env.py`
   - Создать миграцию

2. **Новый сервис**:
   - Создать `App/Services/YourService.py`
   - Добавить dependency в `App/Services/Dependencies.py`

3. **Новый контроллер**:
   - Создать `App/Api/V1/YourController.py`
   - Зарегистрировать в `App/Api/V1/Router.py`

4. **Новая задача планировщика**:
   - Создать `App/Scheduler/Tasks/YourTask.py`
   - Зарегистрировать в `App/Scheduler/TaskRegistry.py`

## Полезные ссылки

- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Alembic: https://alembic.sqlalchemy.org
- APScheduler: https://apscheduler.readthedocs.io
- Scalar: https://github.com/scalar/scalar

