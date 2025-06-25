import logging

from db import engine
from models.base import Base


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


logger = logging.getLogger(__name__)


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("All tables created successfully.")
