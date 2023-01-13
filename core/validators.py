import datetime
import re
import pydantic
import pytz
from config.config import main_settings
from typing import Optional
from fastapi import HTTPException, status

settings = main_settings()


def is_email(value: str, raise_err: bool = True) -> str | bool:
    try:
        pydantic.validate_email(value)
    except pydantic.EmailError as err:
        if raise_err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
        return False
    return value


def is_phone(value: str, raise_err: bool = True) -> str | bool:
    if bool(re.match(correct_phone_pattern(), value)):
        return value
    else:
        if raise_err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Введите корректный номер телефона")
        return False


def correct_phone_pattern():
    return (
        r"^(\+7|7|8|\+8)(\s)?[\s(-]?(9){1}(\d{2})"
        r"[\s)-]?(\s)?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})$"
    )
