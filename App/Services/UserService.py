from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from App.Models.User import User
from App.Schemas.User import UserCreate, UserUpdate
from App.Core.Logger import get_logger


logger = get_logger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        logger.info(f"Получение пользователя по ID: {user_id}")
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        logger.info(f"Получение пользователя по email: {email}")
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        logger.info(f"Получение пользователя по username: {username}")
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        logger.info(f"Получение списка пользователей (skip={skip}, limit={limit})")
        result = await self.session.execute(
            select(User).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, user_data: UserCreate) -> User:
        logger.info(f"Создание нового пользователя: {user_data.username}")
        
        # Проверка на существование
        existing = await self.get_by_email(user_data.email)
        if existing:
            raise ValueError(f"Пользователь с email {user_data.email} уже существует")
        
        existing = await self.get_by_username(user_data.username)
        if existing:
            raise ValueError(f"Пользователь с username {user_data.username} уже существует")
        
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=self._hash_password(user_data.password)
        )
        
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        
        logger.info(f"Пользователь создан: ID={user.id}")
        return user
    
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        logger.info(f"Обновление пользователя ID: {user_id}")
        
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        if 'password' in update_data:
            update_data['hashed_password'] = self._hash_password(update_data.pop('password'))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.session.flush()
        await self.session.refresh(user)
        
        logger.info(f"Пользователь обновлен: ID={user.id}")
        return user
    
    async def delete(self, user_id: int) -> bool:
        logger.info(f"Удаление пользователя ID: {user_id}")
        
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        await self.session.delete(user)
        await self.session.flush()
        
        logger.info(f"Пользователь удален: ID={user_id}")
        return True

