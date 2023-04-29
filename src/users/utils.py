from fastapi import Request, Depends, HTTPException
from passlib.context import CryptContext
from starlette import status
from starlette.responses import JSONResponse

from src import settings
from src.users.actions.auth_actions import get_current_user_from_token
from src.users.models import User
from src.users.schemas.users_schemas import CurrentUserResponseModel


ADMIN_REQUIRED_TEXT: str = "Доступ разрешен только администраторам"
AUTHORIZATION: str = "Authorization"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        return pwd_context.hash(plain_password)


async def get_token_from_cookie(request: Request):
    token = request.cookies.get(AUTHORIZATION)
    if token:
        token = token.split(" ")[1]  # Удаление "Bearer " из значения куки
    return token


async def admin_required(
        user: User = Depends(get_current_user_from_token)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ADMIN_REQUIRED_TEXT,
        )
    return user


def create_auth_response(user: User, access_token: str) -> JSONResponse:
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
