import httpx
import asyncio
import random

from telegram.ext import ExtBot
from injectable import injectable, autowired, Autowired
from loguru import logger
from src.actors.base import IScheduledActor

from src.settings import MemeActorSettings


@injectable(singleton=True)
class MemeSenderActor(IScheduledActor):
    MEME_SUBS = [
        "dankmemes",
        "greentext",
    ]
    MAX_RETRIES = 10

    @autowired
    def __init__(self, settings: Autowired(MemeActorSettings)) -> None:
        self.settings: MemeActorSettings = settings

    async def invoke(self, bot: ExtBot):
        photo_url: str | None = None

        for _ in range(self.MAX_RETRIES):
            sub = random.sample(self.MEME_SUBS, k=1)[0]
            logger.info(f"Fetching meme from r/{sub}")

            try:
                async with httpx.AsyncClient() as client:
                    api_resp = await client.get(f"https://meme-api.com/gimme/{sub}")
                    api_body = api_resp.json()
                    if api_body.get("nsfw"):
                        logger.warning("Skipping NSFW meme")
                        continue

                    photo_url = api_body["url"]
                    break
            except:
                logger.exception("Failed to get meme from API")
                await asyncio.sleep(5)
                continue

        if photo_url is None:
            logger.error(f"Failed to fetch valid meme after {self.MAX_RETRIES} attempts. Aborting")
            return

        logger.info(f"Fetching photo from {photo_url}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(photo_url)
            photo_contents = resp.content

        logger.info("Sending message")
        await bot.send_photo(
            chat_id=self.settings.active_chat_id,
            message_thread_id=self.settings.meme_thread_id,
            caption="Meme of the day",
            photo=photo_contents,
        )

    def schedule(self) -> str | None:
        return None
