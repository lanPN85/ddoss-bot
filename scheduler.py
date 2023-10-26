import asyncio
import logging

from injectable import load_injection_container, autowired, Autowired
from loguru import logger
from telegram.ext import ExtBot

from src.actors.base import IScheduledActor


@autowired
async def main(bot: Autowired(ExtBot), actors: Autowired(list[IScheduledActor])):
    bot: ExtBot = bot
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger.info("Running scheduler...")

    for actor in actors:
        logger.info(f"Scheduling {actor.__class__.__name__}")
        await actor.invoke(bot)
    # await bot.send_photo(
    #     photo="data/test.jpg",
    #     caption="Meme of the day...",
    #     chat_id=settings.active_chat_id,
    #     message_thread_id=settings.meme_thread_id,
    # )


if __name__ == "__main__":
    load_injection_container()
    asyncio.run(main())
