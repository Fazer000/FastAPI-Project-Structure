import sys
import argparse
import uvicorn
from pathlib import Path


# Добавляем корневую директорию в PATH
sys.path.insert(0, str(Path(__file__).parent))


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Запуск FastAPI приложения',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default=None,
        help='Host для запуска сервера (переопределяет .env)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Port для запуска сервера (переопределяет .env)'
    )
    
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Включить автоперезагрузку при изменении файлов'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Количество worker процессов'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default='info',
        choices=['critical', 'error', 'warning', 'info', 'debug', 'trace'],
        help='Уровень логирования uvicorn'
    )
    
    return parser.parse_args()


def main():
    """Главная функция запуска"""
    args = parse_arguments()
    
    # Импортируем настройки после добавления пути
    from App.Core.Config import settings
    
    # Определяем host и port
    host = args.host if args.host is not None else settings.HOST
    port = args.port if args.port is not None else settings.PORT
    
    print("=" * 60)
    print(f"Запуск {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Workers: {args.workers}")
    print(f"Reload: {args.reload}")
    print(f"Log Level: {args.log_level}")
    print("=" * 60)
    
    # Конфигурация uvicorn
    uvicorn_config = {
        "app": "App.Main:app",
        "host": host,
        "port": port,
        "log_level": args.log_level,
        "access_log": True,
    }
    
    # Если reload включен, workers должен быть 1
    if args.reload:
        uvicorn_config["reload"] = True
        uvicorn_config["workers"] = 1
    else:
        uvicorn_config["workers"] = args.workers
    
    # Запуск сервера
    uvicorn.run(**uvicorn_config)


if __name__ == "__main__":
    main()

