from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config


class Database:
    SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # 연결 유효성 미리 확인
        pool_recycle=3600,  # 1시간(3600초)마다 연결 재생성
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()


def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def bootstrap():
    Database.Base.metadata.create_all(bind=Database.engine)
