from sqlalchemy import Column, Integer, Boolean, String, DateTime, BigInteger
from db.database_init import Base, engine


class Settings(Base):
    __tablename__ = 'settings'
    user_id = Column(BigInteger, primary_key=True)
    is_app_configured = Column(Boolean)
    utc_offset = Column(Integer)


class Category(Base):
    __tablename__ = 'categories'
    user_id = Column(BigInteger)
    category_id = Column(String, primary_key=True)
    name = Column(String)
    limit = Column(Integer)


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
