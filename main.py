import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.login.login_handler import register_login

bot = Bot(token='5884965201:AAFiqkenkv-xVTf7GyzUu9sfwGFt5RumUtE', parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


def register_all_handlers():
    register_login(dp)


def on_startup():
    pass


async def main():
    try:
        logging.basicConfig(level=logging.INFO)

        register_all_handlers()

        on_startup()
        await dp.start_polling()

        await bot.get_webhook_info()
    finally:
        await bot.delete_webhook()
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
