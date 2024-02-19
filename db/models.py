import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, BigInteger, UUID, ForeignKey

from db import FFBase
from db.mixins import FetchByIDMixin, CreateObjectMixin

UUID_BASED_ID = Annotated[uuid.UUID, mapped_column(UUID, primary_key=True)]
CREATED_AT = Annotated[datetime, mapped_column(DateTime, default=datetime.utcnow)]
UPDATED_AT = Annotated[
    datetime,
    mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
]


class Profile(FFBase, FetchByIDMixin, CreateObjectMixin):
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    utc_offset: Mapped[int] = mapped_column(default=0)
    categories: Mapped[list['Category'] | None] = relationship(back_populates='profile', )
    expenses: Mapped[list['Expense'] | None] = relationship(back_populates='profile')
    incomes: Mapped[list['Income'] | None] = relationship(back_populates='profile')
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]

    def __init__(self, chat_id: int, utc_offset: int = 0) -> None:
        self.id = chat_id
        self.utc_offset = utc_offset

    '''
    @classmethod
    def create(cls, chat_id: int, utc_offset: int = 0) -> 'Profile':
        new_profile = cls(chat_id, utc_offset)
        cls.session.add(new_profile)
        cls.session.commit()
        return new_profile
    '''

    @classmethod
    def fetch_by_id_or_create(cls, chat_id: int, utc_offset: int = 0) -> 'Profile':
        return cls.fetch_by_id(chat_id) or cls.create(chat_id=chat_id, utc_offset=utc_offset)


class Category(FFBase, CreateObjectMixin):
    __tablename__ = 'categories'
    id: Mapped[UUID_BASED_ID]
    profile_id: Mapped[int] = mapped_column(ForeignKey('profiles.id'))
    profile: Mapped['Profile'] = relationship(back_populates='categories')
    name: Mapped[str] = mapped_column(String(64))
    limit: Mapped[int | None] = mapped_column(default=None)
    expenses: Mapped[list['Expense'] | None] = relationship(back_populates='category')
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]

    def __init__(self, profile_id: int, name: str, limit: int | None = None) -> None:
        self.id = uuid.uuid4()
        self.profile_id = profile_id
        self.name = name
        self.limit = limit

    '''
    @classmethod
    def create(cls, profile_id: int, name: str, limit: int | None = None) -> 'Category':
        new_category = cls(profile_id, name, limit)
        cls.session.add(new_category)
        cls.session.commit()
        return new_category
    '''


class Expense(FFBase):
    __tablename__ = 'expenses'
    id: Mapped[UUID_BASED_ID]
    profile_id: Mapped[int] = mapped_column(ForeignKey('profiles.id'))
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
    profile_id: Mapped[int] = mapped_column(ForeignKey('profiles.id'))
    profile: Mapped['Profile'] = relationship(back_populates='incomes')
    amount: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]


if __name__ == '__main__':
    FFBase.metadata.create_all(bind=FFBase.engine)
