import os
import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums.parse_mode import ParseMode

from handlers.handlers_data import data_router
from handlers.handlers_menu import menu_router
from handlers.handlers_prog import prog_router
from handlers.handlers_profile import profile_router


async def main():
  try:
    bot = Bot(token=os.environ["TOKEN"], parse_mode=ParseMode.HTML)
  except KeyError:
   logging.error("environment variable TOKEN not set")
   sys.exit(1)
  try:
    storage = RedisStorage.from_url(os.environ["REDIS_URL"])
  except KeyError:
    logging.error("environment variable REDIS_URL not set")
    sys.exit(1)
  try:
    dp = Dispatcher(storage=storage)
  except UnboundLocalError:
    logging.error("seems like redis was not connected properly, check if it is running and accessible first")
    sys.exit(1)
  dp.include_router(data_router)
  dp.include_router(prog_router)
  dp.include_router(profile_router)
  dp.include_router(menu_router)
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())
