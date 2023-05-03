from typing import Union

from fastapi import Depends, HTTPException, Request
from jose import JWTError
from jwt import decode
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src import settings
from src.database import get_db
from src.users.dals import UserDAL
from src.users.schemas.users_schemas import CurrentUserResponseModel
from src.security import Hasher
from src.users.models import User


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь не опознан",
)
AUTHORIZATION: str = "Authorization"
ADMIN_REQUIRED_TEXT: str = "Доступ разрешен только администраторам"


async def _get_user_by_email_for_auth(
        email: str, db: AsyncSession) -> Union[User, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_email(email)
            return user


async def authenticate_user(
    login: str, password: str, db: AsyncSession
) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=login, db=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


async def get_token_from_cookie(request: Request):
    token = request.cookies.get(AUTHORIZATION)
    if token:
        token = token.split(" ")[1]  # Удаление "Bearer " из значения куки
    return token


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

    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


async def admin_required(
        user: User = Depends(get_current_user_from_token)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ADMIN_REQUIRED_TEXT,
        )
    return user


def _create_auth_response(user: User, access_token: str) -> JSONResponse:
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CurrentUserResponseModel(
            first_name=user.first_name,
            last_name=user.last_name,
            other_name=user.other_name,
            email=user.email,
            phone=user.phone,
            birthday=user.birthday,
            is_admin=user.is_admin,
        ).dict(),
    )
    response.set_cookie(
        key=AUTHORIZATION,
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return response
