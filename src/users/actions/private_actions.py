from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.users.actions.users_actions import _convert_users_to_list_elements
from src.users.schemas.users_schemas import (UsersListElementModel,
                                             PaginatedMetaDataModel,)
from src.security import Hasher
from src.users.dals import UserDAL, CityDAL
from src.users.schemas.private_schemas import (
    PrivateCreateUserModel,
    PrivateDetailUserResponseModel,
    PrivateUpdateUserModel,
    PrivateUsersListResponseModel,
    CitiesHintModel,
    PrivateUsersListMetaDataModel,
    PrivateUsersListHintMetaModel,
)


EMAIL_EXEPTION_MESSAGE: str = "Почта уже используется"
USER_NOT_FOUND_EXEPTION_MESSAGE: str = "Пользователь не найден"
PHONE_EXEPTION_MESSAGE: str = "Телефон уже используется"
AUTHORIZATION: str = "Authorization"


async def _create_new_user(
        body: PrivateCreateUserModel, db: AsyncSession
) -> PrivateDetailUserResponseModel:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            email_user = await user_dal.get_user_by_email(
                email=body.email
            )
            phone_user = await user_dal.get_user_by_phone(
                phone=body.phone
            )
            if email_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=EMAIL_EXEPTION_MESSAGE
                )
            if phone_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=PHONE_EXEPTION_MESSAGE
                )
            user = await user_dal.create_user(
                first_name=body.first_name,
                last_name=body.last_name,
                other_name=body.other_name,
                email=body.email,
                phone=body.phone,
                birthday=body.birthday,
                city=body.city,
                additional_info=body.additional_info,
                is_admin=body.is_admin,
                hashed_password=Hasher.get_password_hash(
                    body.password
                ),
            )
            return PrivateDetailUserResponseModel.from_orm(user)


async def _update_user_by_id(
        user_id: int,
        body: PrivateUpdateUserModel,
        db: AsyncSession,
) -> PrivateDetailUserResponseModel:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            update_data = body.dict(exclude_unset=True)
            user = await user_dal.update_user(user_id, update_data)
            return PrivateDetailUserResponseModel.from_orm(user)


async def _delete_user_by_id(
        user_id: int, db: AsyncSession) -> bool:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            res = await user_dal.delete_user(user_id)
            return res


async def _get_user_by_id_private(
        user_id: int, db: AsyncSession
) -> PrivateDetailUserResponseModel:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=USER_NOT_FOUND_EXEPTION_MESSAGE
                )
            return PrivateDetailUserResponseModel.from_orm(user)


async def _get_cities(
        session: AsyncSession) -> List[CitiesHintModel]:
    city_dal = CityDAL(session)
    cities = await city_dal.get_cities()
    cities_hints = [
        CitiesHintModel(id=city.id, name=city.name) for city in cities
    ]
    return cities_hints


async def _create_private_users_list_response(
        users_list_elements: List[UsersListElementModel],
        cities_hints: List[CitiesHintModel],
        page: int,
        size: int,
        total: int,
) -> PrivateUsersListResponseModel:
    return PrivateUsersListResponseModel(
        data=users_list_elements,
        meta=PrivateUsersListMetaDataModel(
            pagination=PaginatedMetaDataModel(
                total=total,
                page=page,
                size=size,
            ),
            hint=PrivateUsersListHintMetaModel(
                city=cities_hints
            )
        )
    )


async def _get_users_private(
        page: int, size: int, db: AsyncSession
) -> PrivateUsersListResponseModel:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            total = await user_dal.get_total_users_count()
            users = await user_dal.get_users(page=page, size=size)

            users_list_elements = await _convert_users_to_list_elements(users)
            cities_hints = await _get_cities(session)
            response = await _create_private_users_list_response(
                users_list_elements, cities_hints, page, size, total
            )
            return response
