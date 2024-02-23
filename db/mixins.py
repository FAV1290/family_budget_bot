import uuid
import typing
from datetime import datetime, timedelta

from sqlalchemy.orm import scoped_session, Mapped
from sqlalchemy.sql import extract
from sqlalchemy import select


class FetchByIDMixin:
    id: Mapped[int] | Mapped[uuid.UUID]
    session: scoped_session

    @classmethod
    def fetch_by_id(cls, target_id: int | uuid.UUID) -> typing.Self | None:
        return cls.session.get(cls, target_id)


class CreateMixin:
    session: scoped_session

    @classmethod
    def create(cls, **kwargs: typing.Any) -> typing.Self:
        new_object = cls(**kwargs)
        cls.session.add(new_object)
        cls.session.commit()
        return new_object


class SelfDeleteMixin:
    session: scoped_session

    def delete(self) -> None:
        self.session.delete(self)
        self.session.commit()


class CurrentPeriodUserObjectsMixin:
    session: scoped_session
    profile_id: Mapped[int]
    created_at: Mapped[datetime]

    @classmethod
    def fetch_current_period_objects(
        cls,
        user_id: int,
        user_utc_offset: int,
    ) -> typing.Sequence[typing.Self]:
        user_now = datetime.utcnow() + timedelta(hours=user_utc_offset)
        current_month, current_year = user_now.month, user_now.year
        return cls.session.execute(select(cls).where(
            cls.profile_id == user_id,
            extract('month', cls.created_at) == current_month,
            extract('year', cls.created_at) == current_year,
        )).scalars().all()
