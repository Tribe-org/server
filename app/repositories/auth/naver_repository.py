from urllib.parse import urlencode

import httpx
from fastapi import HTTPException


class NaverRepository:
    def auth_start(self, auth_url, params):
        """
        OAuth 인증 시작 URL을 생성합니다.

        :auth_url OAuth 인증을 시작하기 위한 주소
        :params OAuth 인증에 필요한 파라미터
        :return 완성된 인증 URL
        """
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

    async def delete_token(self, url, headers, params):
        async with httpx.AsyncClient() as client:
            httpx_response = await client.post(url, headers=headers, params=params)
            response = httpx_response.json()

            if response.get("error"):
                raise HTTPException(
                    status_code=response.get("error"),
                    detail=response.get("error_description"),
                )

        return response
