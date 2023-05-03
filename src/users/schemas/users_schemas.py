from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None


class UpdateUserResponseModel(TunedModel):
    id: int
    first_name: str
    last_name: str
    other_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    birthday: Optional[str] = None


class CurrentUserResponseModel(TunedModel):
    first_name: str
    last_name: str
    other_name: Optional[str]
    email: str
    phone: Optional[str]
    birthday: Optional[date]
    is_admin: bool


class UsersListElementModel(TunedModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class PaginatedMetaDataModel(TunedModel):
    total: int
    page: int
    size: int


class UsersListMetaDataModel(TunedModel):
    pagination: PaginatedMetaDataModel


class UsersListResponseModel(TunedModel):
    data: List[UsersListElementModel]
    meta: UsersListMetaDataModel
