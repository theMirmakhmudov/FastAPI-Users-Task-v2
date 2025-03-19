from pydantic import BaseModel
from typing import Optional, Any, List

class Users(BaseModel):
    fullname: str
    username: str
    email: str | None = None
    password: str

class BaseResponse(BaseModel):
    status: bool = True
    data: Optional[Any] = None
    errors: Optional[List[dict]] = None