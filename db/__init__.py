from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

from constants import DB_HOST

class FamilyFundsBotDB:
    def __init__(self, db_host: str) -> None:
        self.engine = create_engine(db_host)
        self.db_session = scoped_session(sessionmaker(bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()
    
    engine = create_engine(DB_HOST)
    db_session = scoped_session(sessionmaker(bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()



class Base(DeclarativeBase):
    engine = create_engine(DB_HOST, pool_size=10)
    db_session = scoped_session(sessionmaker(bind=engine))
    query = db_session.query_property()
