import sys
import subprocess
from pathlib import Path


def apply_migrations():
    """Применение всех миграций"""
    print("=" * 60)
    print("Применение миграций к БД...")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("=" * 60)
            print("✓ Миграции успешно применены!")
            print("=" * 60)
        else:
            print("=" * 60)
            print("✗ Ошибка при применении миграций:")
            print(result.stderr)
            print("=" * 60)
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    apply_migrations()

