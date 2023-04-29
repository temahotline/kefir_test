from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.users.actions.private_actions import USER_NOT_FOUND_EXEPTION_MESSAGE
from src.users.dals import UserDAL
from src.users.models import User
from src.users.schemas.users_schemas import (
    UsersListResponseModel,
    UsersListElementModel,
    UsersListMetaDataModel,
    PaginatedMetaDataModel,
    UpdateUserModel,
    UpdateUserResponseModel,
)


async def _convert_users_to_list_elements(
        users: List[User]) -> List[UsersListElementModel]:
    return [
        UsersListElementModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
        for user in users
    ]


async def _create_users_list_response(
        users_list_elements: List[UsersListElementModel],
        page: int,
        size: int,
        total: int,
) -> UsersListResponseModel:
    return UsersListResponseModel(
        data=users_list_elements,
        meta=UsersListMetaDataModel(
            pagination=PaginatedMetaDataModel(
                total=total,
                page=page,
                size=size,
            )
        )
    )


async def _get_users(
        page: int, size: int, session: AsyncSession
) -> UsersListResponseModel:
    async with session.begin():
        user_dal = UserDAL(session)
        total = await user_dal.get_total_users_count()
        users = await user_dal.get_users(page=page, size=size)

        users_list = await _convert_users_to_list_elements(users)
        response = await _create_users_list_response(
            users_list, page, size, total)
        return response


async def _update_user(
        user_id: int,
        body: UpdateUserModel,
        session: AsyncSession,
) -> UpdateUserResponseModel:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND_EXEPTION_MESSAGE
            )
        update_data = body.dict(exclude_none=True)
        updated_user = await user_dal.update_user(user, **update_data)
        return UpdateUserResponseModel(**updated_user.__dict__)

