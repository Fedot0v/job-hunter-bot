from typing import Sequence

from sqlalchemy import select, delete

from base_repo import BaseRepository
from db.models.vacancies import Keyword


class KeywordRepository(BaseRepository):
    async def get_all(self) -> Sequence[Keyword]:
        stmt = select(Keyword)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_code(self, code: str) -> Sequence[Keyword]:
        stmt = select(Keyword).where(Keyword.code == code)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
    
    async def add(self, keyword: Keyword) -> Keyword:
        await self.db_session.add(keyword)
        await self.db_session.flush()
        return keyword
    
    async def delete(self, code: str) -> None:
        stmt = delete(Keyword).where(Keyword.code == code)
        await self.db_session.execute(stmt)
        await self.db_session.flush()
