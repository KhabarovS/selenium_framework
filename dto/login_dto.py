from typing import Optional

from pydantic import StrictStr, Field

from api.services.reqres_in.reqres_in import ReqresIn


class LoginResponse(ReqresIn):
    """ Схема авторизации пользователя """
    token: Optional[StrictStr] = Field(...)
    error: Optional[StrictStr] = Field(...)
