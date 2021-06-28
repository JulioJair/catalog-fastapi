from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(description="Password hashed")


class UserCreate(UserBase):
    pass
    class Config():
        orm_mode = True


# Properties to receive via API on update
class UserUpdate(UserBase):
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool] = Field(
        1, description="Is the user account active?")
    is_admin: Optional[bool] = Field(1, description="Is the user admin?")


# Properties to return to client
class UserOut(BaseModel):
    full_name: str
    email: EmailStr

    class Config():
        orm_mode = True
