from datetime import date
from typing import List

from pydantic import BaseModel, EmailStr


class UpdateUserModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: str


class UpdateUserResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: str


class CurrentUserResponseModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: date
    is_admin: bool


class UsersListElementModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class PaginatedMetaDataModel(BaseModel):
    total: int
    page: int
    size: int


class UsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel


class UsersListResponseModel(BaseModel):
    data: List[UsersListElementModel]
    meta: UsersListMetaDataModel
