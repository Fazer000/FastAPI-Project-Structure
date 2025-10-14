from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from App.Core.Database import get_db_session
from App.Services.UserService import UserService


async def get_user_service(
    session: AsyncSession = None
) -> AsyncGenerator[UserService, None]:
    if session is None:
        async for db_session in get_db_session():
            yield UserService(db_session)
    else:
        yield UserService(session)

