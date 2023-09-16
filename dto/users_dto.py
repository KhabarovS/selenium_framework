from datetime import datetime
from typing import Optional

from pydantic import StrictInt, EmailStr, StrictStr, Field

from dto.generic import ReqresDto


class UsersDto(ReqresDto):
    """ Схема пользователя """
    id_: StrictInt = Field(alias='id')
    email: EmailStr
    first_name: StrictStr
    last_name: StrictStr
    avatar: StrictStr


class SupportDto(ReqresDto):
    """ Схема поддержки """
    url: StrictStr
    text: StrictStr


class UserResponseDto(ReqresDto):
    """ Схема ответа одиночного пользователя """
    data: UsersDto
    support: SupportDto


class UsersListResponseDto(ReqresDto):
    """ Схема ответа со списком пользователей """
    page: StrictInt
    per_page: StrictInt
    total: StrictInt
    data: Optional[list[UsersDto]] = Field(...)


class RequestUserDto(ReqresDto):
    """ Схема запроса создания/обновления пользователя """
    name: StrictStr
    job: StrictStr


class UpdateUserDto(RequestUserDto):
    """ Схема ответа обновления пользователя """
    createdAt: datetime


class CreateUserDto(UpdateUserDto):
    """ Схема ответа создания пользователя """
    id_: StrictStr = Field(alias='id')