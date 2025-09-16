#!/usr/bin/env python3
"""
Универсальный скрипт запуска FastAPI проекта.
Поддерживает разные режимы запуска и автоматическую настройку окружения.
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path
from typing import List, Optional


class ProjectRunner:
    """Класс для управления запуском проекта."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_module = "app.main:app"
        self.default_host = "127.0.0.1"
        self.default_port = 8000
    
    def check_python_version(self) -> bool:
        """Проверка версии Python."""
        if sys.version_info < (3, 9):
            print("❌ Требуется Python 3.9 или выше")
            return False
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        return True
    
    def check_dependencies(self) -> bool:
        """Проверка установленных зависимостей."""
        try:
            import fastapi
            import uvicorn
            print("✅ Основные зависимости установлены")
            return True
        except ImportError as e:
            print(f"❌ Отсутствуют зависимости: {e}")
            return False
    
    def install_dependencies(self, use_poetry: bool = False) -> bool:
        """Установка зависимостей."""
        print("📦 Установка зависимостей...")
        
        if use_poetry and shutil.which("poetry"):
            cmd = ["poetry", "install"]
        else:
            cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        
        try:
            subprocess.run(cmd, check=True, cwd=self.project_root)
            print("✅ Зависимости установлены")
            return True
        except subprocess.CalledProcessError:
            print("❌ Ошибка установки зависимостей")
            return False
    
    def setup_env_file(self) -> None:
        """Создание .env файла из примера."""
        env_file = self.project_root / ".env"
        env_example = self.project_root / "env.example"
        
        if not env_file.exists() and env_example.exists():
            shutil.copy(env_example, env_file)
            print("✅ Создан .env файл из примера")
            print("⚠️  Не забудь настроить переменные окружения в .env")
    
    def run_development(self, host: str, port: int, reload: bool = True) -> None:
        """Запуск в режиме разработки."""
        print(f"🚀 Запуск в режиме разработки на http://{host}:{port}")
        
        cmd = [
            "uvicorn",
            self.app_module,
            "--host", host,
            "--port", str(port),
        ]
        
        if reload:
            cmd.append("--reload")
        
        os.environ["ENVIRONMENT"] = "development"
        subprocess.run(cmd, cwd=self.project_root)
    
    def run_production(self, host: str, port: int, workers: int = 4) -> None:
        """Запуск в продакшн режиме."""
        print(f"🏭 Запуск в продакшн режиме на http://{host}:{port}")
        
        cmd = [
            "uvicorn",
            self.app_module,
            "--host", host,
            "--port", str(port),
            "--workers", str(workers),
            "--access-log",
        ]
        
        os.environ["ENVIRONMENT"] = "production"
        subprocess.run(cmd, cwd=self.project_root)
    
    def run_tests(self) -> None:
        """Запуск тестов."""
        print("🧪 Запуск тестов...")
        
        if not shutil.which("pytest"):
            print("❌ pytest не установлен")
            return
        
        cmd = ["pytest", "-v"]
        subprocess.run(cmd, cwd=self.project_root)
    
    def lint_code(self) -> None:
        """Проверка кода линтерами."""
        print("🔍 Проверка кода...")
        
        # Black
        if shutil.which("black"):
            print("Форматирование с Black...")
            subprocess.run(["black", "app/"], cwd=self.project_root)
        
        # isort
        if shutil.which("isort"):
            print("Сортировка импортов с isort...")
            subprocess.run(["isort", "app/"], cwd=self.project_root)
        
        # flake8
        if shutil.which("flake8"):
            print("Проверка с flake8...")
            subprocess.run(["flake8", "app/"], cwd=self.project_root)
    
    def show_info(self) -> None:
        """Показать информацию о проекте."""
        print("📋 Информация о проекте:")
        print(f"   Корневая папка: {self.project_root}")
        print(f"   Модуль приложения: {self.app_module}")
        print(f"   Python версия: {sys.version}")
        
        # Проверка файлов
        files_to_check = [".env", "requirements.txt", "pyproject.toml"]
        for file in files_to_check:
            path = self.project_root / file
            status = "✅" if path.exists() else "❌"
            print(f"   {file}: {status}")


def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(description="Универсальный скрипт запуска FastAPI проекта")
    
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    
    # Команда dev
    dev_parser = subparsers.add_parser("dev", help="Запуск в режиме разработки")
    dev_parser.add_argument("--host", default="127.0.0.1", help="Хост (по умолчанию: 127.0.0.1)")
    dev_parser.add_argument("--port", type=int, default=8000, help="Порт (по умолчанию: 8000)")
    dev_parser.add_argument("--no-reload", action="store_true", help="Отключить автоперезагрузку")
    
    # Команда prod
    prod_parser = subparsers.add_parser("prod", help="Запуск в продакшн режиме")
    prod_parser.add_argument("--host", default="0.0.0.0", help="Хост (по умолчанию: 0.0.0.0)")
    prod_parser.add_argument("--port", type=int, default=8000, help="Порт (по умолчанию: 8000)")
    prod_parser.add_argument("--workers", type=int, default=4, help="Количество воркеров")
    
    # Команда install
    install_parser = subparsers.add_parser("install", help="Установка зависимостей")
    install_parser.add_argument("--poetry", action="store_true", help="Использовать Poetry")
    
    # Другие команды
    subparsers.add_parser("test", help="Запуск тестов")
    subparsers.add_parser("lint", help="Проверка и форматирование кода")
    subparsers.add_parser("info", help="Информация о проекте")
    
    args = parser.parse_args()
    
    runner = ProjectRunner()
    
    # Проверка Python версии
    if not runner.check_python_version():
        sys.exit(1)
    
    if args.command == "dev":
        if not runner.check_dependencies():
            print("Попробуй: python run.py install")
            sys.exit(1)
        
        runner.setup_env_file()
        runner.run_development(
            host=args.host,
            port=args.port,
            reload=not args.no_reload
        )
    
    elif args.command == "prod":
        if not runner.check_dependencies():
            print("Попробуй: python run.py install")
            sys.exit(1)
        
        runner.setup_env_file()
        runner.run_production(
            host=args.host,
            port=args.port,
            workers=args.workers
        )
    
    elif args.command == "install":
        runner.install_dependencies(use_poetry=args.poetry)
    
    elif args.command == "test":
        runner.run_tests()
    
    elif args.command == "lint":
        runner.lint_code()
    
    elif args.command == "info":
        runner.show_info()
    
    else:
        print("🚀 Универсальный скрипт запуска FastAPI проекта")
        print("\nДоступные команды:")
        print("  dev     - Запуск в режиме разработки")
        print("  prod    - Запуск в продакшн режиме")
        print("  install - Установка зависимостей")
        print("  test    - Запуск тестов")
        print("  lint    - Проверка кода")
        print("  info    - Информация о проекте")
        print("\nПримеры:")
        print("  python run.py dev")
        print("  python run.py dev --port 8080")
        print("  python run.py prod --workers 8")
        print("  python run.py install")


if __name__ == "__main__":
    main()
