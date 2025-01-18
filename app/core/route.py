from logging import getLogger
from typing import Any, Callable, Dict

from fastapi import Request, Response
from fastapi.routing import APIRoute


class LoggingAPIRoute(APIRoute):
    """API 요청 로깅 객체"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.api_logger = getLogger(name="api_logger")

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:

            # 요청 로깅
            await self._request_log(request=request)

            # router 에 따라 서비스 로직 처리
            response: Response = await original_route_handler(request)

            # 응답 로깅
            self._response_log(request=request, response=response)

            return response

        return custom_route_handler

    def _has_json_body(self, request: Request) -> bool:
        """json 요청 여부 확인"""
        if (
            request.method in ("POST", "PUT", "PATCH")
            and request.headers.get("content-type") == "application/json"
        ):
            return True
        return False

    async def _request_log(self, request: Request) -> None:
        """요청 로깅"""
        extra: Dict[str, Any] = {
            "httpMethod": request.method,
            "url": request.url.path,
            "headers": request.headers,
            "queryParams": request.query_params,
        }

        if self._has_json_body(request):
            request_body = await request.body()
            extra["body"] = request_body.decode("UTF-8")

        self.api_logger.info(f"request {extra}")

    def _response_log(self, request: Request, response: Response) -> None:
        """응답 로깅"""
        extra: Dict[str, str | int] = {
            "httpMethod": request.method,
            "url": request.url.path,
            "statusCode": response.status_code,
            "body": response.body.decode("UTF-8"),  # type: ignore
        }

        self.api_logger.info(f"response {extra}")
