from pydantic import BaseModel, Field, EmailStr, validator, validate_email, EmailError
from typing import Optional
from fastapi import HTTPException, status


class PostCreateSchema(BaseModel):
    head: str
    main_text: str


class PostUpdate(BaseModel):
    head: Optional[str]
    main_text: Optional[str]


class PostOutBase(BaseModel):
    status: int
    detail: str


class PostCreateOut(PostOutBase):
    pass


class PostUpdateOut(PostOutBase):
    pass


class PostDeleteOut(PostOutBase):
    pass
