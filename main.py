import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage

from app.config import settings
from app.handlers.cancel_command import router as cancel_router
from app.handlers.incomes import router as incomes_router
from app.handlers.other_handlers import router as other_router
from app.handlers.spendings import router as spendings_router
from app.handlers.start_commands import router as start_router
from app.handlers.statistics import router as stat_router
from app.logging import setup_logger
from app.menu import set_main_menu


async def main():

    bot = Bot(settings.BOT_API)
    redis = Redis(host=settings.REDIS_HOST)
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    dp.include_router(router=cancel_router)
    dp.include_router(router=spendings_router)
    dp.include_router(router=incomes_router)
    dp.include_router(router=stat_router)
    dp.include_router(router=start_router)
    dp.include_router(router=other_router)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        setup_logger("INFO")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemError):
        print("Бот был остановлен")
