from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bot.common.date import transform_date
from bot.handlers.login.login_handler import get_default_reply_markup
from database.schedule.schedule_datastore import get_schedules_by_dep_id, student_get_schedules_message, \
    teacher_get_schedules_message
from database.user.user_datastore import get_role_by_chat_id

schedule_callback = CallbackData('schedule_id_callback', 'id', 'c_id')


async def schedules_message(message: types.Message):
    schedules = get_schedules_by_dep_id(1)
    schedules_inline_keyboard = []

    for schedule in schedules:
        schedules_inline_keyboard.append([
            InlineKeyboardButton(
                transform_date(str(schedule['date'])),
                callback_data=schedule_callback.new(id=schedule['id'], c_id=message.chat.id)
            )
        ])

    await message.answer('📅 Выберите день',
                         reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=schedules_inline_keyboard))


async def schedule_callback_message(call: types.CallbackQuery, callback_data: dict):
    schedule_id = callback_data.get('id')
    c_id = callback_data.get('c_id')
    role = get_role_by_chat_id(c_id).text.replace('"', "")
    message = ''

    if role == "STUDENT":
        message = student_get_schedules_message(c_id, schedule_id)
    elif role == "TEACHER":
        message = teacher_get_schedules_message(c_id, schedule_id)

    await call.message.answer(message, reply_markup=get_default_reply_markup())


def register_schedule(dp: Dispatcher):
    dp.register_message_handler(schedules_message, (lambda message: message.text == 'Расписание 🕘'))
    dp.register_callback_query_handler(schedule_callback_message, schedule_callback.filter())
