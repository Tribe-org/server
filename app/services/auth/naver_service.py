from app.core import Config
from app.repositories import NaverRepository
from app.utils import generate_state

from .auth_service import AuthService

naver_repository = NaverRepository()


class NaverService(AuthService):
    def auth_start(self):
        naver_auth_url = "https://nid.naver.com/oauth2.0/authorize"
        state = generate_state()

        params = {
            "response_type": "code",
            "client_id": Config.NAVER_CLIENT_ID,
            "redirect_uri": Config.NAVER_REDIRECT_URL,
            "state": state,
        }

        return naver_repository.auth_start(auth_url=naver_auth_url, params=params)

    async def auth_callback(self, code: str, state: str):
        url = "https://nid.naver.com/oauth2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
        data = {
            "grant_type": "authorization_code",
            "client_id": Config.NAVER_CLIENT_ID,
            "client_secret": Config.NAVER_CLIENT_SECRET,
            "redirect_uri": Config.NAVER_REDIRECT_URL,
            "code": code,
            "state": state,
        }

        return await naver_repository.auth_callback(url, headers, data)

    async def user_me(self, access_token: str):
        url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}

        return await naver_repository.user_me(url, headers)
