import asyncio
import logging
import sys

from loader import dp, bot
import handlers  # noqa
from utils.notify_admins import on_startup_notify

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup_notify(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
