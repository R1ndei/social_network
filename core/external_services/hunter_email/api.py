from config.config import main_settings
from fastapi import HTTPException, status
import httpx

from core.schemas.external_services.common import HunterResponse

settings = main_settings()


async def verifying_email(email: str) -> HunterResponse:
    async with httpx.AsyncClient() as client:
        params = {'email': email, 'api_key': settings.HUNTER_API_KEY}
        response = await client.get('https://api.hunter.io/v2/email-verifier', params=params)
        return HunterResponse(response=response.json(), status_code=response.status_code)
