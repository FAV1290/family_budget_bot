from sqlalchemy import Column, Integer, Boolean, ARRAY, String, DateTime, BigInteger
from database_init import Base, engine


class Settings(Base):
    __tablename__ = 'settings'
    user_id = Column(BigInteger, primary_key=True)
    is_app_configured = Column(Boolean)
    utc_offset = Column(Integer)


class Categories(Base):
    __tablename__ = 'categories'
    user_id = Column(BigInteger, primary_key=True)
    user_categories = Column(ARRAY(String))


class Expense(Base):
    __tablename__ = 'expenses'
    user_id = Column(BigInteger)
    expense_id = Column(String, primary_key=True)
    created_at = Column(DateTime)
    amount = Column(Integer)
    category = Column(String)
    description = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
