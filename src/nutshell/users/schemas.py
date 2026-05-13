from pydantic import BaseModel, ConfigDict, EmailStr, Field

from nutshell.enums import UserRole


class UserCreate(BaseModel):
  username: str = Field(..., min_length=3, max_length=30)
  email: EmailStr
  password: str = Field(..., min_length=8)



class UserAuth(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: UserRole


class LoginRequest(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"


class TokenData(BaseModel):
  user_id: int | None = None
