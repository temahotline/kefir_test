from pydantic import BaseModel


class LoginModel(BaseModel):
    login: str
    password: str
