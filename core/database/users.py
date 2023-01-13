from asyncpg import UniqueViolationError
from fastapi import HTTPException
from starlette import status

from config.config import main_settings
from config.db_config import database
from core import validators
from core.auth.auth_logic import HashPassword, format_phone_for_db
from core.schemas.auth.common import RegisterSchema
from core.utils import moscow_time_now
from resources.users.models import User

settings = main_settings()


async def get_user(username: str) -> User:
    if validators.is_email(username):
        return await User.objects.get_or_none(email=username)
    username = await format_phone_for_db(username)
    if validators.is_phone(username):
        return await User.objects.get_or_none(phone=username)
    return None


async def get_superuser(username: str) -> User:
    if validators.is_email(username):
        return await User.objects.get_or_none(email=username, is_super_user=True)

    return await User.objects.get_or_none(phone=username, is_super_user=True)


async def create_user(user_data: RegisterSchema) -> User:
    async with database.transaction():
        try:
            user_data.password = HashPassword.bcrypt(user_data.password)
            user_data.phone = await format_phone_for_db(user_data.phone)
            user = await User.objects.create(**user_data.dict(), created_at=await moscow_time_now())
            return user
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone number or email already in use",
            )

# async def send_email_or_phone(instance: User = None):
#     if check_email(instance['email']):
#         user_in_db = await get_user_without_exceptions(instance['email'])
#         if user_in_db:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Указанная почта уже существует")
#         try:
#             # Deactivate send email during tests
#             if os.environ.get("TESTING") != "1":
#                 await send_email(email=[instance['email']], instance=instance)
#             return {"status": 200,
#                     "contact_type": "email",
#                     "value": instance['email']}
#         except ConnectionErrors as e:
#             raise HTTPException(status_code=400, detail="Something wrong with sender")
#     instance['phone'] = await format_phone_for_db(instance['phone'])
#     if check_phone(instance['phone']):
#         full_response = await send_new_sms(instance['phone'])
#         return {"status": 200, "contact_type": "phone", "value": instance['phone'],
#                 "full_response": full_response}
#     raise HTTPException(status_code=400, detail="Введите корректный телефон или email!")
