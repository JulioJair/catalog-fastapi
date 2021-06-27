from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    hashed_password: str = Field(description="Password hashed")
    is_active: Optional[bool] = Field(
        1, description="Is the user account active?")
    is_admin: Optional[bool] = Field(1, description="Is the user admin?")


class User(UserBase):
    class Config():
        orm_mode = True


# Properties to receive via API on update
class UserUpdate(UserBase):
    full_name: Optional[str]
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    is_active: Optional[bool]
    is_admin: Optional[bool]


# Properties to return to client
class UserIndex(User):
    pass


# Properties to return to client
class UserShow(User):
    pass
