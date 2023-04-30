from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None


class UpdateUserResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    other_name: Optional[str]
    email: str
    phone: Optional[str]
    birthday: Optional[str]


class CurrentUserResponseModel(BaseModel):
    first_name: str
    last_name: str
    other_name: Optional[str]
    email: str
    phone: Optional[str]
    birthday: Optional[date]
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
