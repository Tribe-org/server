import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from starlette.middleware.sessions import SessionMiddleware

from app.core import Config, database_bootstrap
from app.routers.router import main_router

# 환경 변수에서 스테이지 가져오기 (대문자는 그대로 유지)
stage_env = Config.ENV.value

# URL 경로에 사용하기 위해 소문자로 변환
stage_url = stage_env.lower()

# API URL 설정
base_api_url = os.getenv("BASE_API_URL", "http://localhost:8000")

# 데이터베이스 설정
database_bootstrap()

# FastAPI 앱 생성
app = FastAPI(
    docs_url="/v1/docs",
    openapi_url="/v1/openapi.json",
    root_path=f"/{stage_url}",  # URL 경로에는 소문자 사용
)


# Swagger(OpenAPI) 명세 커스터마이징
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Swagger 서버 정보 추가 (URL에 소문자 스테이지 사용)
    servers = [
        {
            "url": f"{base_api_url}/{stage_url}",
            "description": f"{stage_env} environment",  # 설명에는 대문자 스테이지 사용
        }
    ]

    # OpenAPI 스키마 생성
    openapi_schema = get_openapi(
        title="TRIBE",
        version="0.0.1",
        description="API Documentation",
        routes=app.routes,
    )
    openapi_schema["servers"] = servers
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# 커스터마이징 된 OpenAPI 설정 적용
app.openapi = custom_openapi

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=Config.APP_SECRET_KEY,
    # 1시간 후 세션 만료
    max_age=3600,
)

# 라우트 설정
app.include_router(main_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# AWS Lambda용 핸들러 설정
handler = Mangum(app)
