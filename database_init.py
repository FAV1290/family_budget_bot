from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from constants import DB_LOGIN, DB_PASSWORD, DB_NAME


engine = create_engine(
    f'postgresql://{DB_LOGIN}:{DB_PASSWORD}@hattie.db.elephantsql.com/{DB_NAME}'
)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()