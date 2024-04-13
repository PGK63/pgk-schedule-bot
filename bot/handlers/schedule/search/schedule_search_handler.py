from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.handlers.schedule.search.state.teacher_schedule_search_state import TeacherScheduleSearchState
from bot.handlers.schedule.search.teacher_schedule_search_handler import register_teacher_schedule_search_handler

schedule_search_type = CallbackData('schedule_search_type', 'type')


# Schedule id
# teacher id


async def schedule_search(message: types.Message):
    await message.answer(
        text='Выберите тип',
        disable_notification=True,
        reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                InlineKeyboardButton(text='Группа 👥', callback_data=schedule_search_type.new(type='group'))
            ],
            [
                InlineKeyboardButton(text='Преподаватель 👤', callback_data=schedule_search_type.new(type='teacher'))
            ]
        ])
    )


async def start_search(call: types.CallbackQuery, callback_data: dir):
    search_type = callback_data.get('type')

    if search_type == 'group':
        await call.message.answer('Скоро появится...', disable_notification=True)
    elif search_type == 'teacher':
        await call.message.answer(
            "✏️ Отправьте фамилию (имя отчество по желанию) преподавателя",
            disable_notification=True
        )
        await TeacherScheduleSearchState.StartSearch.set()


def register_schedule_search(dp: Dispatcher):
    dp.register_message_handler(schedule_search, (lambda message: message.text == 'Поиск 🔎'))
    dp.register_callback_query_handler(start_search, schedule_search_type.filter())

    register_teacher_schedule_search_handler(dp)
