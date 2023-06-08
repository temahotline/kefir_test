from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.models import User
from src.users.actions.auth_actions import admin_required
from src.users.actions.private_actions import (
    _get_users_private,
    _create_new_user,
    _get_user_by_id_private,
    _update_user_by_id,
    _delete_user_by_id,
)
from src.users.schemas.private_schemas import (
    PrivateUsersListResponseModel,
    PrivateDetailUserResponseModel,
    PrivateCreateUserModel,
    PrivateUpdateUserModel,
)


private_router = APIRouter()


@private_router.get(
    "/users",
    response_model=PrivateUsersListResponseModel,
    status_code=200,
)
async def get_users(
    page: int = Query(1, gt=0),
    size: int = Query(20, gt=0),
    user: User = Depends(admin_required),
    session: AsyncSession = Depends(get_db),
):
    return await _get_users_private(
        page=page, size=size, session=session,
    )


@private_router.post(
    "/users",
    response_model=PrivateDetailUserResponseModel,
    status_code=201,
)
async def create_user(
    body: PrivateCreateUserModel,
    user: User = Depends(admin_required),
    session: AsyncSession = Depends(get_db),
):
    return await _create_new_user(body=body, session=session)


@private_router.get(
    "/users/{user_id}",
    response_model=PrivateDetailUserResponseModel,
    status_code=200,
)
async def get_user(
    user_id: int,
    user: User = Depends(admin_required),
    session: AsyncSession = Depends(get_db),
):
    return await _get_user_by_id_private(
        user_id=user_id, session=session,
    )


@private_router.patch(
    "/users/{user_id}",
    response_model=PrivateDetailUserResponseModel,
    status_code=200,
)
async def update_user(
    user_id: int,
    body: PrivateUpdateUserModel,
    user: User = Depends(admin_required),
    session: AsyncSession = Depends(get_db),
):
    return await _update_user_by_id(
        user_id=user_id, body=body, session=session,
    )


@private_router.delete(
    "/users/{user_id}",
    status_code=204,
)
async def delete_user(
    user_id: int,
    user: User = Depends(admin_required),
    session: AsyncSession = Depends(get_db),
):
    is_deleted = await _delete_user_by_id(
        user_id=user_id, session=session,
    )
    if is_deleted:
        return JSONResponse(status_code=204, content={})
