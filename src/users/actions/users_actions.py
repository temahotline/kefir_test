from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

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


USER_NOT_FOUND_EXEPTION_MESSAGE: str = "Пользователь не найден"


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
        page: int, size: int, db: AsyncSession
) -> UsersListResponseModel:
    async with db as session:
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
        db: AsyncSession,
) -> UpdateUserResponseModel:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            update_data = body.dict(exclude_unset=True)
            await user_dal.update_user(
                user_id=user_id,
                update_data=update_data,
            )
            user = await user_dal.get_user_by_id(user_id)
            return UpdateUserResponseModel.from_orm(user)
