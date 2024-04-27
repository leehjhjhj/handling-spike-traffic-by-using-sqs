from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_scoped_session, create_async_engine, async_sessionmaker
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
schema = os.environ.get('DB_SCHEMA')

def get_async_mysql_uri():
    return f"mysql+aiomysql://{user}:{password}@{host}:{port}/{schema}?charset=utf8mb4"

def get_sync_mysql_uri():
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}?charset=utf8mb4"

def get_sqlite_uri():
    return "sqlite:///./sqlite.db"

Base = declarative_base()
DB_URL = get_sync_mysql_uri()

engine = create_async_engine(get_async_mysql_uri(), echo=True)
session_factory = async_sessionmaker(bind=engine)
AsyncSession = async_scoped_session(session_factory, scopefunc=asyncio.current_task)