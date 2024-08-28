from sqlalchemy.orm import declarative_base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import db_url


Base = declarative_base()


engine = create_async_engine(db_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)