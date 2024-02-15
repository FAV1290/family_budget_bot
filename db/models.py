from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, BigInteger, UUID, ForeignKey

from db import FFBase


UUID_BASED_ID = Annotated[UUID, mapped_column(primary_key=True)]
CREATED_AT = Annotated[DateTime, mapped_column(default=datetime.utcnow)]
UPDATED_AT = Annotated[DateTime, mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)]


class Profile(FFBase):
    __tablename__ = 'profiles'
    id: Mapped[BigInteger] = mapped_column(primary_key=True)
    utc_offset: Mapped[int] = mapped_column(default=0)
    categories: Mapped[list['Category'] | None] = relationship(back_populates='profile')
    expenses: Mapped[list['Expense'] | None] = relationship(back_populates='profile')
    incomes: Mapped[list['Income'] | None] = relationship(back_populates='profile')
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]


class Category(FFBase):
    __tablename__ = 'categories'
    id: Mapped[UUID_BASED_ID]
    profile_id: Mapped[BigInteger] = mapped_column(ForeignKey('profiles.id'))
    profile: Mapped['Profile'] = relationship(back_populates='categories')
    name: Mapped[str] = mapped_column(String(64))
    limit: Mapped[int | None] = mapped_column(default=None)
    expenses: Mapped[list['Expense'] | None] = relationship(back_populates='category')
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]


class Expense(FFBase):
    __tablename__ = 'expenses'
    id: Mapped[UUID_BASED_ID]
    profile_id: Mapped[BigInteger] = mapped_column(ForeignKey('profiles.id'))
    profile: Mapped['Profile'] = relationship(back_populates='expenses')
    amount: Mapped[int] = mapped_column()
    category_id: Mapped[UUID] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='expenses')
    description: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]


class Income(FFBase):
    __tablename__ = 'incomes'
    id: Mapped[UUID_BASED_ID]
    profile_id: Mapped[BigInteger] = mapped_column(ForeignKey('profiles.id'))
    profile: Mapped['Profile'] = relationship(back_populates='incomes')
    amount: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]


if __name__ == '__main__':
    FFBase.metadata.create_all(bind=FFBase.engine)
