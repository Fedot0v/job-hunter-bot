from typing import Sequence

from sqlalchemy import select

from repositories.base_repo import BaseRepository
from db.models.vacancies import Vacancy, Keyword


class VacancyRepository(BaseRepository):
    async def get_all(self) -> Sequence[Vacancy]:
        stmt = select(Vacancy)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_code(self, code: str) -> Sequence[Vacancy]:
        stmt = (
            select(Vacancy)
            .join(Vacancy.keyword)
            .where(Keyword.code == code)
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
    
    async def add(self, vacancy: Vacancy) -> Vacancy:
        self.db_session.add(vacancy)
        await self.db_session.flush()
        return vacancy
    
    async def get_by_link(self, link: str) -> Vacancy | None:
        stmt = select(Vacancy).where(Vacancy.link == link)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_by_link(self, link: str) -> None:
        vacancy = await self.get_by_link(link)
        if vacancy:
            await self.db_session.delete(vacancy)
            await self.db_session.flush()
        else:
            raise ValueError(f"Vacancy with link {link} not found.")
