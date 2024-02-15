from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

from constants import DB_HOST


class FFBase(DeclarativeBase):
    engine = create_engine(DB_HOST)
    db_session = scoped_session(sessionmaker(bind=engine))
    query = db_session.query_property()
