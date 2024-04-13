import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.handlers.schedule.schedule_handler import get_schedules_keyboard, schedule_action_callback, schedule_callback
from bot.handlers.schedule.search.state.student_schedule_search_state import StudentScheduleSearchState
from database.schedule.schedule_datastore import get_schedules, student_get_schedules_message_group_name


async def input_group_name(message: types.Message, state: FSMContext):
    group_name = message.text.strip().upper()

    if re.findall("^(([А-Я]{2}|[А-Я]{3})-([0-9]{2}|[0-9]{3}))$", group_name):
        await state.update_data(group_name=group_name)

        await message.answer('📅 Выберите день', disable_notification=True,
                             reply_markup=types.InlineKeyboardMarkup(
                                 row_width=1,
                                 inline_keyboard=get_all_schedules_keyboard(0, message.chat.id)))
    else:
        await message.answer('❌ Неверный формат группы')


async def update_schedules_group_name(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get("action")
    current_page = int(callback_data.get("page"))
    c_id = callback_data.get("c_id")

    if action == 'next':
        current_page += 1
    elif action == 'back':
        current_page -= 1

    await call.message.edit_text('📅 Выберите день', disable_web_page_preview=True,
                                 reply_markup=types.InlineKeyboardMarkup(
                                     row_width=1,
                                     inline_keyboard=get_all_schedules_keyboard(current_page, c_id)
                                 ))


async def input_schedule_students_search(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    state_date = await state.get_data()
    group_name = state_date.get('group_name')
    schedule_id = callback_data['id']
    schedule_message = student_get_schedules_message_group_name(group_name, schedule_id)
    await state.finish()
    await call.message.answer(schedule_message, disable_notification=True)


def get_all_schedules_keyboard(page, chat_id):
    schedule = get_schedules(page)
    return get_schedules_keyboard(schedule, page, chat_id)


def register_student_schedule_search_handler(dp: Dispatcher):
    dp.register_message_handler(input_group_name, state=StudentScheduleSearchState.StartSearch)

    dp.register_callback_query_handler(update_schedules_group_name, schedule_action_callback.filter(),
                                       state=StudentScheduleSearchState.StartSearch)

    dp.register_callback_query_handler(input_schedule_students_search, schedule_callback.filter(),
                                       state=StudentScheduleSearchState.StartSearch)
