from .base import IDatabaseHelper
from src.model import Award, MessageKey
import asyncpg
from asyncpg.pool import Pool
from asyncio import Lock
from datetime import date
from injectable import injectable, Autowired, autowired

from src.settings import PostgresSettings


@injectable(singleton=True, primary=True)
class PostgresDatabaseHelper(IDatabaseHelper):
    @autowired
    def __init__(self, settings: Autowired(PostgresSettings)) -> None:
        self.postgres_dsn = settings.dsn()
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

    async def insert_award(self, award: Award) -> int:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO awards(from_user, to_user, type_, chat_name, message, awarded_at)
                VALUES($1, $2, $3, $4, $5, $6)
                """,
                award.from_user,
                award.to_user,
                award.type_,
                award.chat_name,
                award.message,
                award.awarded_at,
            )

    async def count_user_awards_today(self, user_name: str) -> int:
        today = date.today()
        pool = await self._get_pool()

        async with pool.acquire() as conn:
            result = await conn.fetchval(
                """
                SELECT COUNT(id)
                FROM awards
                WHERE from_user = $1
                    AND DATE(awarded_at) = $2
                """,
                user_name,
                today,
            )
            return result
