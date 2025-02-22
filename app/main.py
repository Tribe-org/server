from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.middleware.sessions import SessionMiddleware

from app.core import Config, EnvTypes, OpenAPI, database_bootstrap
from app.routers.router import main_router
import os
from fastapi.openapi.utils import get_openapi
stage_env = Config.ENV.value
# URL 경로에 사용하기 위해 소문자로 변환
stage_url = stage_env.lower()

# 환경 변수에서 스테이지 가져오기 (대문자는 그대로 유지)



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/#lifespan
    FastAPI Server 생명주기를 컨트롤 하는 함수
    """
    # Server Start Up Event
    if Config.ENV == EnvTypes.DEV:
        # NOTE - meta.create_all 보다는 Alembic 을 활용하여
        # NOTE - 버전별 스키마 마이그레이션을 하는게 좋습니다만
        # NOTE - Alembic 을 활용하기에는 배 보다 배꼽이 크므로 일단 if 문 처리
        database_bootstrap()  # 모든 DB 테이블 생성
    yield
    # Server Shut down Event


# FastAPI 앱 생성
app = FastAPI(
    docs_url="/v1/docs",
    openapi_url="/v1/openapi.json",
    root_path=f"/{stage_url}",  # URL 경로에는 소문자 사용
)
# 데이터베이스 설정
database_bootstrap()


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
app.include_router(main_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# AWS Lambda용 핸들러 설정
handler = Mangum(app)
