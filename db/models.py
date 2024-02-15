from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, UUID, ForeignKey

from db import FFBase


class Profile(FFBase):
    __tablename__ = 'profiles'
    id: Mapped[BigInteger] = mapped_column(primary_key=True)
    utc_offset: Mapped[int] = mapped_column(default=0)
    categories: Mapped[list['Category'] | None] = relationship(back_populates='profile')
    expenses: Mapped[list['Expense'] | None] = relationship(back_populates='profile')
    incomes: Mapped[list['Income'] | None] = relationship(back_populates='profile')


class Category(FFBase):
    __tablename__ = 'categories'
    id: Mapped[UUID] = mapped_column(primary_key=True)
    profile_id: Mapped[BigInteger] = mapped_column(ForeignKey('profiles.id'))
    profile: Mapped['Profile'] = relationship(back_populates='categories')
    name: Mapped[str] = mapped_column(String(64))
    limit: Mapped[int | None] = mapped_column(default=None)


class Expense(FFBase):
    __tablename__ = 'expenses'
    id: Mapped[UUID] = mapped_column(primary_key=True)
    profile_id: Mapped[BigInteger] = mapped_column(ForeignKey('profiles.id'))
    profile = relationship('Profile', back_populates='expenses')
    created_at = Column(DateTime)
    amount = Column(Integer)
    category = Column(String)
    description = Column(String)


class Income(FFBase):
    __tablename__ = 'incomes'
    id: Mapped[UUID] = mapped_column(primary_key=True)
    profile_id: Mapped[BigInteger] = mapped_column(ForeignKey('profiles.id'))
    profile = relationship('Profile', back_populates='incomes')
    created_at = Column(DateTime)
    amount = Column(Integer)
    description = Column(String)


if __name__ == '__main__':
    FFBase.metadata.create_all(bind=FFBase.engine)
