from abc import ABC, abstractmethod
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException


class AuthRepository(ABC):
    @abstractmethod
    def auth_start(self, auth_url, params):
        """
        OAuth 인증 시작 URL을 생성합니다.

        :auth_url OAuth 인증을 시작하기 위한 주소
        :params OAuth 인증에 필요한 파라미터
        :return 완성된 인증 URL
        """
        pass

    @abstractmethod
    async def auth_callback(self, url, headers, data):
        pass
