from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from .auth_repository import AuthRepository


class NaverRepository(AuthRepository):
    def auth_start(self, auth_url, params):
        query_string = urlencode(params)
        url = f"{auth_url}?{query_string}"

        return url

    async def auth_callback(self, url, headers, data):
        async with httpx.AsyncClient() as client:
            httpx_response = await client.post(url, headers=headers, data=data)
            response = httpx_response.json()

            if response.get("error"):
                raise HTTPException(status_code=500, detail="에러 나중에 처리해야 함")

        return response

    async def user_me(self, url, headers):
        async with httpx.AsyncClient() as client:
            httpx_response = await client.get(url, headers=headers)
            response = httpx_response.json()

        return response
