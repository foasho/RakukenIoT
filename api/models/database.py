from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf.env import Env

SQLALCHEMY_DATABASE_URL = f"mysql://{Env('DB_USER')}:{Env('DB_PWD')}@{Env('DB_HOST')}/{Env('DB_NAME')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"connect_timeout": 15}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""
DB Session
"""
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()