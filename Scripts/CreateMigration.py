import sys
import subprocess
from pathlib import Path


def create_migration():
    """Создание новой миграции с описанием"""
    if len(sys.argv) < 2:
        print("Использование: python Scripts/CreateMigration.py 'Описание миграции'")
        sys.exit(1)
    
    message = sys.argv[1]
    
    print("=" * 60)
    print(f"Создание миграции: {message}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", message],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("=" * 60)
            print("✓ Миграция успешно создана!")
            print("=" * 60)
        else:
            print("=" * 60)
            print("✗ Ошибка при создании миграции:")
            print(result.stderr)
            print("=" * 60)
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_migration()

