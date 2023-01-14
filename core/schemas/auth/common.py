from fastapi import HTTPException, status
from pydantic import BaseModel, Field, EmailStr, validator

from core.validators import is_email, is_phone


class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterSchema(BaseModel):
    phone: str
    email: EmailStr
    password: str
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    mid_name: str

    @validator('phone')
    def phone_match(cls, v):
        return is_phone(v)

    @validator('email')
    def email_match(cls, v):
        email = is_email(v)
        return email

    @validator('password')
    def password_match(cls, v):
        if len(v) < 7:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password must be at least 7 characters long")
        return v


class RegisterOutSchema(BaseModel):
    status: int = Field(200, title="Status registration code")
    value: str = Field(..., title="Contact value")
