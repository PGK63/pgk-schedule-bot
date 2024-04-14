import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from bot.handlers.schedule.schedule_handler import get_schedules_keyboard
from bot.handlers.schedule.search.state.student_schedule_search_state import StudentScheduleSearchState
from database.schedule.schedule_datastore import get_schedules, student_get_schedules_message_group_name

schedule_search_student_callback = CallbackData('schedule_search_student_callback', 'id', 'c_id', 'teacher_id', 'group_name')
schedule_search_student_action_callback = CallbackData('schedule_search_student_action_callback', 'action', 'page', 'c_id', 'group_name')


async def input_group_name(message: types.Message, state: FSMContext):
    group_name = message.text.strip().upper()

    if re.findall("^(([А-Я]{2}|[А-Я]{3})-([0-9]{2}|[0-9]{3}))$", group_name):
        await state.finish()

        await message.answer('📅 Выберите день', disable_notification=True,
                             reply_markup=types.InlineKeyboardMarkup(
                                 row_width=1,
                                 inline_keyboard=get_all_schedules_keyboard(0, message.chat.id, group_name)))
    else:
        await message.answer('❌ Неверный формат группы')


async def update_schedules_group_name(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get("action")
    current_page = int(callback_data.get("page"))
    c_id = callback_data.get("c_id")
    group_name = callback_data.get("group_name")

    if action == 'n':
        current_page += 1
    elif action == 'b':
        current_page -= 1

    await call.message.edit_text('📅 Выберите день', disable_web_page_preview=True,
                                 reply_markup=types.InlineKeyboardMarkup(
                                     row_width=1,
                                     inline_keyboard=get_all_schedules_keyboard(current_page, c_id, group_name)
                                 ))


async def input_schedule_students_search(call: types.CallbackQuery, callback_data: dict):
    group_name = callback_data['group_name']
    schedule_id = callback_data['id']
    schedule_message = student_get_schedules_message_group_name(group_name, schedule_id)
    await call.message.answer(schedule_message, disable_notification=True)


def get_all_schedules_keyboard(page, chat_id, group_name):
    schedules = get_schedules(page)
    return get_schedules_keyboard(schedules, chat_id,
                                  group_name=group_name,
                                  schedule_callback_data=schedule_search_student_callback,
                                  next_action_callback_new=schedule_search_student_action_callback.new(
                                      action='n', page=page, c_id=chat_id, group_name=group_name),
                                  back_action_callback_new=schedule_search_student_action_callback.new(
                                      action='b', page=page, c_id=chat_id, group_name=group_name)
                                  )


def register_student_schedule_search_handler(dp: Dispatcher):
    dp.register_message_handler(input_group_name, state=StudentScheduleSearchState.StartSearch)

    dp.register_callback_query_handler(update_schedules_group_name, schedule_search_student_action_callback.filter())
    dp.register_callback_query_handler(input_schedule_students_search, schedule_search_student_callback.filter())
