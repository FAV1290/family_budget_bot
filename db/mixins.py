import uuid
import typing

from sqlalchemy.orm import scoped_session, Mapped


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
