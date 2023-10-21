from .base import IDatabaseHelper
from src.model import MessageKey, MessageType
import asyncpg
from asyncpg.pool import Pool
from asyncio import Lock


class PostgresDatabaseHelper(IDatabaseHelper):
    def __init__(self, postgres_dsn: str) -> None:
        self.postgres_dsn = postgres_dsn
        self.pool: Pool | None = None
        self.pool_lock = Lock()

    async def _get_pool(self) -> Pool:
        async with self.pool_lock:
            if self.pool is not None:
                return self.pool
            self.pool = await asyncpg.create_pool(
                dsn=self.postgres_dsn, min_size=1, max_size=3
            )
            return self.pool

    async def increment_message_count(self, key: MessageKey):
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO user_message_stats(date_, chat_name, user_name, topic_name, type_)
                VALUES($1, $2, $3, $4, $5)
                ON CONFLICT (date_, chat_name, user_name, topic_name, type_)
                DO
                UPDATE SET message_count = user_message_stats.message_count + 1
                """,
                key.date,
                key.chat_name,
                key.user_name,
                key.topic_name,
                key.type_,
            )
