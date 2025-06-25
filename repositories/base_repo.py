from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        """
        Initializes the BaseRepository with a database session.

        Args:
            db_session (AsyncSession): An asynchronous database session.
        """
        self.db_session = db_session
