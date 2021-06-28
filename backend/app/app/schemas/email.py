from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class Email(BaseModel):
    email: List[EmailStr]
