import datetime

import ormar

from config.db_config import MainMetaDB
from core.utils import moscow_time


class User(ormar.Model):
    class Meta(MainMetaDB):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True, nullable=False)
    phone: str = ormar.String(max_length=50, unique=True, nullable=False)
    email: str = ormar.String(max_length=100, unique=True, nullable=False)
    password: str = ormar.String(max_length=500, nullable=False)
    first_name: str = ormar.String(max_length=100, nullable=False, default="")
    last_name: str = ormar.String(max_length=100, nullable=False, default="")
    mid_name: str = ormar.String(max_length=100, nullable=False, default="")
    created_at: datetime.datetime = ormar.DateTime(default=moscow_time, nullable=False)
    is_verified: bool = ormar.Boolean(default=False)
    is_super_user: bool = ormar.Boolean(default=False, nullable=False)
    is_verified_email: bool = ormar.Boolean(default=False, nullable=False)
