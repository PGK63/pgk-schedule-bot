import asyncio
import locale

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.errors_handler import register_errors_handler
from bot.handlers.login.login_handler import register_login
from bot.handlers.schedule.schedule_handler import register_schedule
from bot.handlers.schedule.schedule_time_handler import register_schedule_time_handler
from bot.handlers.schedule.search.schedule_search_handler import register_schedule_search
from bot.handlers.user.user_handler import register_user
from bot.services.setting_commands import set_default_commands

bot = Bot(token='7700309962:AAGlhS_7nU9zEp7cKhevBYdq3kKF7ZRfLhk', parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


async def set_all_default_commands():
    await set_default_commands(bot=bot)


def register_all_handlers():
    register_login(dp)
    register_schedule(dp)
    register_schedule_time_handler(dp)
    register_user(dp)
    register_schedule_search(dp)
    register_errors_handler(dp)


def on_startup():
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


async def main():
    try:
        await set_all_default_commands()
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
