from pydantic import BaseModel

class Users(BaseModel):
    fullname: str
    username: str
    email: str | None = None
    password: str

class BaseResponse(BaseModel):
    status: bool
    body: str | list | dict | None = None
    error: str | None = None