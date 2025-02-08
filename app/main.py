import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.middleware.sessions import SessionMiddleware

from app.core import Config, OpenAPI, database_bootstrap
from app.routers.router import main_router

# 환경 변수로부터 스테이지를 가져와 root_path를 설정
stage = os.getenv("STAGE", "dev")  # 기본값은 dev
root_path = f"/{stage}"

# 데이터베이스 설정
database_bootstrap()

app = FastAPI(
    docs_url=f"{root_path}/v1/docs",
    openapi_url=f"{root_path}/v1/openapi.json",
    root_path=root_path,
)

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
app.include_router(main_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# AWS Lambda용 핸들러 설정
handler = Mangum(app)
