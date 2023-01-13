import datetime
import uuid
from enum import Enum

moscow_time = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
moscow_time_format = moscow_time.strftime('%Y.%m.%dT%X')
moscow_time_strip = moscow_time.strftime("%f%X%d%m%y").replace(":", "")


async def moscow_time_now():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3)
