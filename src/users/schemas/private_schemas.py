import re
from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr, constr, validator

from src.users.schemas.users_schemas import UsersListElementModel, PaginatedMetaDataModel


PHONE_REGEX_PATTERN: str = r"(\+7|8)[0-9]{10}"
PHONE_REGEX = re.compile(PHONE_REGEX_PATTERN)
PHONE_VALIDATION_ERROR: str = "Неверный формат номера телефона"


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class PrivateCreateUserModel(BaseModel):
    first_name: constr(
        strip_whitespace=True, min_length=1, max_length=50,
    )
    last_name: constr(
        strip_whitespace=True, min_length=1, max_length=50,
    )
    other_name: Optional[constr(
        strip_whitespace=True, min_length=1, max_length=50,
    )] = None
    email: EmailStr
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[int] = None
    additional_info: Optional[str] = None
    is_admin: bool
    password: str

    @validator("phone", allow_reuse=True)
    def validate_phone(cls, phone):
        if phone and not re.fullmatch(PHONE_REGEX, phone):
            raise ValueError(PHONE_VALIDATION_ERROR)
        return phone


class PrivateUpdateUserModel(BaseModel):
    id: int
    first_name: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=50)
    ] = None
    last_name: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=50)
    ] = None
    other_name: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=50)
    ] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[int] = None
    additional_info: Optional[str] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None

    @validator("phone")
    def validate_phone(cls, phone):
        if not None and not re.fullmatch(PHONE_REGEX, phone):
            raise ValueError(PHONE_VALIDATION_ERROR)
        return phone


class PrivateDetailUserResponseModel(TunedModel):
    id: int
    first_name: str
    last_name: str
    other_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[int] = None
    additional_info: Optional[str] = None
    is_admin: bool


class CitiesHintModel(TunedModel):
    id: int
    name: str


class PrivateUsersListHintMetaModel(TunedModel):
    city: List[CitiesHintModel]


class PrivateUsersListMetaDataModel(TunedModel):
    pagination: PaginatedMetaDataModel
    hint: PrivateUsersListHintMetaModel


class PrivateUsersListResponseModel(TunedModel):
    data: List[UsersListElementModel]
    meta: PrivateUsersListMetaDataModel
