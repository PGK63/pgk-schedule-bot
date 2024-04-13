from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from bot.handlers.login.login_handler import get_teachers_reply_markup, teacher_callback
from bot.handlers.schedule.schedule_handler import get_schedules_keyboard, schedule_callback, schedule_action_callback
from bot.handlers.schedule.search.state.teacher_schedule_search_state import TeacherScheduleSearchState
from database.schedule.schedule_datastore import get_schedules_by_teacher_id, \
    teacher_get_schedules_message_by_teacher_id


async def start_teacher_search(message: types.Message):
    await message.answer(
        "👤 Выберите ФИО из списка\n\nНажмите 'Назад', чтобы попробовать еще раз",
        disable_notification=True,
        reply_markup=get_teachers_reply_markup(name=message.text)
    )


async def input_teacher_search(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    teacher_id = callback_data.get('id')
    if teacher_id == "back":
        await call.message.edit_text(
            "✏️ Отправьте фамилию (имя отчество по желанию) преподавателя"
        )
    else:
        await state.update_data(teacher_id=teacher_id)

        await call.message.answer('📅 Выберите день', disable_notification=True,
                                  reply_markup=InlineKeyboardMarkup(
                                      row_width=1,
                                      inline_keyboard=get_schedules_keyboard_by_teacher_id(teacher_id, 0,
                                                                                           call.message.chat.id)
                                  ))


async def update_schedules_by_teacher_id(call: types.CallbackQuery, callback_data: dir):
    action = callback_data.get("action")
    current_page = int(callback_data.get("page"))
    teacher_id = callback_data.get("teacher_id")
    c_id = callback_data.get("c_id")

    if action == 'next':
        current_page += 1
    elif action == 'back':
        current_page -= 1

    await call.message.edit_text('📅 Выберите день', disable_web_page_preview=True,
                                 reply_markup=InlineKeyboardMarkup(
                                     row_width=1,
                                     inline_keyboard=get_schedules_keyboard_by_teacher_id(teacher_id, current_page, c_id)
                                 ))


async def input_schedule_teachers_search(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    state_date = await state.get_data()
    teacher_id = state_date.get('teacher_id')
    schedule_id = callback_data['id']
    schedule_message = teacher_get_schedules_message_by_teacher_id(schedule_id, teacher_id)
    await state.finish()
    await call.message.answer(schedule_message, disable_notification=True)


def get_schedules_keyboard_by_teacher_id(teacher_id, page, chat_id):
    schedule = get_schedules_by_teacher_id(teacher_id, page)
    return get_schedules_keyboard(schedule, page, chat_id, teacher_id=teacher_id)


def register_teacher_schedule_search_handler(dp: Dispatcher):
    dp.register_message_handler(start_teacher_search, state=TeacherScheduleSearchState.StartSearch)

    dp.register_callback_query_handler(input_teacher_search, teacher_callback.filter(),
                                       state=TeacherScheduleSearchState.StartSearch)

    dp.register_callback_query_handler(input_schedule_teachers_search, schedule_callback.filter(),
                                       state=TeacherScheduleSearchState.StartSearch)

    dp.register_callback_query_handler(update_schedules_by_teacher_id, schedule_action_callback.filter(),
                                       state=TeacherScheduleSearchState.StartSearch)
