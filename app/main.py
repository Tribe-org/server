from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.middleware.sessions import SessionMiddleware

from app.core import Config, EnvTypes, OpenAPI, database_bootstrap
from app.routers.router import main_router


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


app = FastAPI(docs_url="/api/docs", lifespan=lifespan)


# 스웨거 설정
app.openapi = OpenAPI(app).get_customized_openapi

# CORS 설정 추가
origins = [Config.CLIENT_URL]

# 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
