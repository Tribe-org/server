from fastapi.openapi.utils import get_openapi


class OpenAPI:
    def __init__(self, app):
        self.app = app
        self.exclude_paths = [
            "/refresh-token",
        ]

    def is_in_exclude_path(self, path: str):
        for exclude_path in self.exclude_paths:
            if exclude_path in path:
                return True
        return False

    def get_customized_openapi(self):
        if self.app.openapi_schema:
            return self.app.openapi_schema

        openapi_schema = get_openapi(
            title="트라이브 API 문서", version="1.0.0", routes=self.app.routes
        )

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }

        # 특정 경로를 제외하고 BearerAuth 적용
        for path in openapi_schema["paths"]:
            if self.is_in_exclude_path(path):
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["security"] = [
                        {"BearerAuth": []}
                    ]
        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema
