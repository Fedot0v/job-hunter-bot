from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String, ForeignKey

from base import BaseModel


class Vacancy(BaseModel):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    company: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    experience: Mapped[str] = mapped_column(nullable=True)
    skills: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=True,
        default=list
    )
    link: Mapped[str] = mapped_column(unique=True, nullable=False)
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey("keywords.id"),
        nullable=False
    )
    keyword: Mapped["Keyword"] = relationship(
        "Keyword",
        back_populates="vacancies",
        lazy="joined"
    )


class Keyword(BaseModel):
    __tablename__ = "keywords"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    vacancies: Mapped[List[Vacancy]] = relationship(
        "Vacancy",
        back_populates="keyword",
        lazy="joined"
    )