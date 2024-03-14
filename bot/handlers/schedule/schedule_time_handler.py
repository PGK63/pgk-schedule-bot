from aiogram import types, Dispatcher


async def schedule_time(message: types.Message):
    await message.answer('🕘 <b>1 Смена</b>\n\n'
                         '1 пара 08:30-09:50\n'
                         '2 пара 10:00-11:20\n'
                         'Обед 11:20-12:00\n'
                         '3 пара 12:00-13:20\n'
                         '4 пара 13:30-14:50\n'
                         '5 пара 15:00-16:20\n'
                         '\n'
                         '🕘 <b>2 Смена</b>\n\n'
                         '1 пара 13:30-14:50\n'
                         '2 пара 15:00-16:20\n'
                         '3 пара 16:35-17:55\n'
                         '4 пара 18:05-19:25\n')


def register_schedule_time_handler(dp: Dispatcher):
    dp.register_message_handler(schedule_time, (lambda message: message.text == 'Расписание звонков 🕘'))
