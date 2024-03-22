from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bot.common.date import transform_date
from bot.handlers.login.login_handler import get_default_reply_markup
from database.schedule.schedule_datastore import get_schedules_by_dep_id, student_get_schedules_message, \
    teacher_get_schedules_message
from database.user.user_datastore import get_role_by_chat_id

schedule_callback = CallbackData('schedule_id_callback', 'id', 'c_id')
schedule_action_callback = CallbackData('schedule_id_callback', 'action', 'page', 'dep_id', 'c_id')


async def schedules_message(message: types.Message):
    await message.answer('📅 Выберите день', disable_notification=True,
                         reply_markup=InlineKeyboardMarkup(
                             row_width=1, inline_keyboard=get_schedules_keyboard(1, 0, message.chat.id)))


async def update_schedules(call: types.CallbackQuery, callback_data: dir):
    action = callback_data.get("action")
    current_page = int(callback_data.get("page"))
    dep_id = callback_data.get("dep_id")
    c_id = callback_data.get("c_id")
    if action == 'next':
        current_page += 1
    elif action == 'back':
        current_page -= 1
    await call.message.edit_text('📅 Выберите день', disable_web_page_preview=True,
                                 reply_markup=InlineKeyboardMarkup(
                                     row_width=1,
                                     inline_keyboard=get_schedules_keyboard(dep_id, current_page, c_id)))


def get_schedules_keyboard(dep_id, page, c_id):
    schedules = get_schedules_by_dep_id(dep_id, page)
    schedules_inline_keyboard = []

    for schedule in schedules['content']:
        schedules_inline_keyboard.append([
            InlineKeyboardButton(
                transform_date(str(schedule['date'])),
                callback_data=schedule_callback.new(id=schedule['id'], c_id=c_id)
            )
        ])

    if not bool(schedules['last']):
        schedules_inline_keyboard.append({
            InlineKeyboardButton(
                'Дальше ➡️',
                callback_data=schedule_action_callback.new(action='next', page=page, dep_id=dep_id, c_id=c_id)
            )
        })

    if not bool(schedules['first']):
        schedules_inline_keyboard.append({
            InlineKeyboardButton(
                '⬅️ Назад',
                callback_data=schedule_action_callback.new(action='back', page=page, dep_id=dep_id, c_id=c_id)
            )
        })

    return schedules_inline_keyboard


async def schedule_callback_message(call: types.CallbackQuery, callback_data: dict):
    schedule_id = callback_data.get('id')
    c_id = callback_data.get('c_id')
    role = get_role_by_chat_id(c_id).text.replace('"', "")
    message = ''

    if role == "STUDENT":
        message = student_get_schedules_message(c_id, schedule_id)
    elif role == "TEACHER":
        message = teacher_get_schedules_message(c_id, schedule_id)

    await call.message.answer(message, disable_notification=True, reply_markup=get_default_reply_markup())


def register_schedule(dp: Dispatcher):
    dp.register_message_handler(schedules_message, (lambda message: message.text == 'Расписание 🕘'))
    dp.register_callback_query_handler(schedule_callback_message, schedule_callback.filter())
    dp.register_callback_query_handler(update_schedules, schedule_action_callback.filter())
