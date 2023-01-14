from pydantic import BaseModel


class HunterResponse(BaseModel):
    response: dict
    status_code: int
