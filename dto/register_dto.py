from typing import Optional

from pydantic import StrictInt, Field, StrictStr

from api.services.reqres_in.reqres_in import ReqresIn


class RegisterResponse(ReqresIn):
    """ Схема регистрации пользователя """
    id_: Optional[StrictInt] = Field(..., by_alias='id')
    token: Optional[StrictStr] = Field(...)
    error: Optional[StrictStr] = Field(...)
