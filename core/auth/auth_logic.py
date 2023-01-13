from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from passlib.context import CryptContext
from config.config import main_settings
from core import validators
from core.schemas.auth.common import Token
from resources.users.models import User

PASSWORD_CONTEXT = CryptContext(schemes="bcrypt")
settings = main_settings()

auth_scheme = OAuth2PasswordBearer(tokenUrl=settings.API_PATH_V1 + "authorization/" + "login", scopes={
    "common": "Common access",
})


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(auth_scheme),
) -> Union[User, None]:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невозможно проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub", None)
        token_scopes = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
    except JWTError:
        raise credentials_exception

    user = await get_user(username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_superuser(
        user: User = Depends(get_current_user),
) -> Union[User, None]:
    credentials_exception_not_superuser = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await get_superuser(user.email)
    if user is None:
        raise credentials_exception_not_superuser
    return user


class HashPassword:
    @staticmethod
    def bcrypt(password: str) -> str:
        return PASSWORD_CONTEXT.hash(password)

    @staticmethod
    def verify(hashed_password: str, input_password: str) -> bool:
        return PASSWORD_CONTEXT.verify(input_password, hashed_password)


async def check_user(phone_or_email: str, password: str, scopes: Optional[list] = None) -> Token:
    user: User = await get_user(phone_or_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )
    if not HashPassword.verify(user.password, password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wrong email or password"
        )
    access_token = create_access_token(data={"sub": phone_or_email, "scopes": scopes})
    return Token(access_token=access_token, token_type="bearer")


async def get_user(username: str) -> User:
    if validators.is_email(username, False):
        return await User.objects.get_or_none(email=username)
    username = await format_phone_for_db(username)
    if validators.is_phone(username, False):
        return await User.objects.get_or_none(phone=username)


async def get_superuser(username: str) -> User:
    if validators.is_email(username):
        return await User.objects.get_or_none(email=username, is_super_user=True)

    return await User.objects.get_or_none(phone=username, is_super_user=True)


async def format_phone_for_db(phone: str) -> str:
    replace_ch = "+()- "
    for i in replace_ch:
        phone = phone.replace(i, "")
    if phone[0] == "8":
        new_phone = f"7{phone[1:]}"
        return new_phone
    return phone
