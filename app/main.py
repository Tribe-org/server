from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core import Config, OpenAPI, database_bootstrap
from app.routers.router import main_router

# 데이터베이스 설정
database_bootstrap()

app = FastAPI()

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
