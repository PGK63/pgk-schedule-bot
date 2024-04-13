import logging

from aiogram import Dispatcher


async def errors_handler(update, exception):
    if update.message:
        await update.message.reply(f'Ошибка: {exception}', disable_notification=True)
    else:
        logging.error(f'Ошибка обработки обновления: {exception}')


def register_errors_handler(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
