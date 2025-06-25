from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, DateTime, func, String, Column
from sqlalchemy.orm import relationship

from base import BaseModel


user_vacancy = Table(
    "user_vacancy",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("vacancy_id", ForeignKey("vacancies.id"), primary_key=True)
)


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(server_default=func.now())
    
    saved_jobs: Mapped[List["Vacancy"]] = relationship(
        "Vacancy",
        secondary=user_vacancy,
        backref="saved_by_users",
        lazy="joined"
    )
