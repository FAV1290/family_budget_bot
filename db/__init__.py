from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

from constants import DB_HOST


class FFBase(DeclarativeBase):
    engine = create_engine(DB_HOST)
    session = scoped_session(sessionmaker(bind=engine))
    query = session.query_property() # Should it be?
 