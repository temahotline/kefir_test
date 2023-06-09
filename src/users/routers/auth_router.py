from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src import settings
from src.database import get_db
from src.security import create_access_token
from src.users.models import User
from src.users.schemas.auth_schemas import LoginModel
from src.users.schemas.users_schemas import CurrentUserResponseModel
from src.users.actions.auth_actions import (
    authenticate_user,
    get_current_user_from_token,
    _create_auth_response,
)


auth_router = APIRouter()
INCORRECT_EMAIL_OR_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 400,
            "message": "Incorrect email or password"},
)


@auth_router.post("/login", response_model=CurrentUserResponseModel)
async def login(
        login_model: LoginModel,
        session: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(
        login_model.login, login_model.password, session
    )
    if user is None:
        raise INCORRECT_EMAIL_OR_PASSWORD
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return _create_auth_response(user, access_token)


@auth_router.get("/logout", status_code=200)
async def logout(
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_db)
) -> Response:
    response = Response(status_code=200)
    response.delete_cookie(key="Authorization")
    return response
