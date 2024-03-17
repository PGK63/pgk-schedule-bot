from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    await bot.delete_my_commands()
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', 'Перезапустить бот 📌'),
            BotCommand('profile', 'Информация о регистрации 👤'),
        ],
        scope=BotCommandScopeDefault()
    )