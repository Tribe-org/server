from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config


class Database:
    SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
