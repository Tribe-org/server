from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config

db_session_context: ContextVar[Optional[int]] = ContextVar(
    "db_session_context", default=None
)


class Database:
    SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    @staticmethod
    def get_session():
        return Database.SessionLocal()


def get_db():
    db = Database.get_session()
    try:
        yield db
    finally:
        db.close()


def bootstrap():
    Database.Base.metadata.create_all(bind=Database.engine)


def db(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session = db_session_context.get()
        return func(*args, **kwargs, session=db_session)

    return wrap_func


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Database.get_session()
    db_session_context.set(session)
    try:
        yield session
        session.commit()
    except Exception as exc:
        print(exc)
        session.rollback()
        raise exc
    finally:
        session.close()
        db_session_context.set(None)
