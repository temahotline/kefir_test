from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.actions.auth_actions import get_current_user_from_token
from src.users.actions.users_actions import _get_users, _update_user
from src.users.models import User
from src.users.schemas.users_schemas import (
    UsersListResponseModel,
    CurrentUserResponseModel,
    UpdateUserResponseModel,
    UpdateUserModel,
)


users_router = APIRouter()


@users_router.get(
    "/", response_model=UsersListResponseModel, status_code=200)
async def get_users(
    page: int = Query(1, gt=0),
    size: int = Query(20, gt=0),
    db: AsyncSession = Depends(get_db),
):
    return await _get_users(page=page, size=size, db=db)


@users_router.get(
    "/current",
    response_model=CurrentUserResponseModel,
    status_code=200,
)
async def get_current_user(
    user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    return user


@users_router.patch(
    "/current",
    response_model=UpdateUserResponseModel,
    status_code=200,
)
async def update_current_user(
    body: UpdateUserModel,
    user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    return await _update_user(user_id=user.id, body=body, db=db)
