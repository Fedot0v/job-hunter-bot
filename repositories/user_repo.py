

from sqlalchemy import select, delete

from repositories.base_repo import BaseRepository
from db.models.users import User, user_vacancy


class UserRepository(BaseRepository):
    async def add(self, user: User) -> User:
        await self.db_session.add(user)
        await self.db_session.flush()
        return user
    
    async def add_to_favorites(self, user_id: int, vacancy_id: int) -> None:
        stmt = (
            user_vacancy.insert().values(
                user_id=user_id,
                vacancy_id=vacancy_id
            )
        )
        await self.db.session.execute(stmt)
        await self.db_session.flush()

    async def remove_from_favorites(self, user_id: int, vacancy_id: int) -> None:
        stmt = (
            delete(user_vacancy)
            .where(
                user_vacancy.c.user_id == user_id,
                user_vacancy.c.vacancy_id == vacancy_id
            )
        )
        await self.db_session.execute(stmt)
        await self.db_session.flush()

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()
