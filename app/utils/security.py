"""Утилиты безопасности и JWT."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import UnauthorizedException


# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Получение хеша пароля."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """Проверка JWT токена."""
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        raise UnauthorizedException("Invalid token")


def decode_access_token(token: str) -> Optional[str]:
    """Декодирование токена доступа."""
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise UnauthorizedException("Invalid token payload")
        return username
    except JWTError:
        raise UnauthorizedException("Could not validate credentials")


class SecurityUtils:
    """Утилиты безопасности."""
    
    @staticmethod
    def generate_token_data(user_id: int, username: str) -> Dict[str, Any]:
        """Генерация данных для токена."""
        return {
            "sub": username,
            "user_id": user_id,
            "iat": datetime.utcnow(),
        }
    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        """Проверка силы пароля."""
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return all([has_upper, has_lower, has_digit, has_special])
