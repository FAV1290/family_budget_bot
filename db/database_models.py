from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, UUID, ForeignKey

from db import FFBase


class Profile(FFBase):
    __tablename__ = 'profiles'
    id = Column(BigInteger, primary_key=True)
    utc_offset = Column(Integer)
    categories = relationship('Category', back_populates='profile')
    expenses = relationship('Expense', back_populates='profile')


class Category(FFBase):
    __tablename__ = 'categories'
    id = Column(UUID, primary_key=True)
    profile_id = ForeignKey('profiles.id')
    name = Column(String)
    limit = Column(Integer)


class Expense(FFBase):
    __tablename__ = 'expenses'
    id = Column(BigInteger)
    expense_id = Column(UUID, primary_key=True)
    created_at = Column(DateTime)
    amount = Column(Integer)
    category = Column(String)
    description = Column(String)


class Income(FFBase):
    __tablename__ = 'incomes'
    id = Column(BigInteger)
    income_id = Column(UUID, primary_key=True)
    created_at = Column(DateTime)
    amount = Column(Integer)
    description = Column(String)


if __name__ == "__main__":
    FFBase.metadata.create_all(bind=FFBase.engine)
