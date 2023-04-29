from typing import Union

from fastapi import Depends, HTTPException
from jose import JWTError
from jwt import decode
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src import settings
from src.database import get_db
from src.users.dals import UserDAL
from src.users.models import User
from src.users.utils import Hasher, get_token_from_cookie


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь не опознан",
)


async def _get_user_by_email_for_auth(
        email: str, session: AsyncSession) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_email(email)
        return user


async def authenticate_user(
    login: str, password: str, db: AsyncSession
) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=login, session=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


async def get_current_user_from_token(
        token: str = Depends(get_token_from_cookie),
        db: AsyncSession = Depends(get_db)
):
    if not token:
        raise CREDENTIALS_EXCEPTION

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION

    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user
