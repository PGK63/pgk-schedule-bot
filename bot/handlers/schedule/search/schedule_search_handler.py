from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.handlers.schedule.schedule_handler import schedules_message
from bot.handlers.schedule.search.state.teacher_schedule_search_state import TeacherScheduleSearchState

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


async def start_search(call: types.CallbackQuery):
    if call.message == 'Группа 👥':
        await call.message.answer('Скоро появится...')
    elif call.message == 'Преподаватель 👤':
        await schedules_message(call.message)
        await TeacherScheduleSearchState.InputSchedule.set()


def register_schedule_search(dp: Dispatcher):
    dp.register_message_handler(schedule_search, (lambda message: message.text == 'Поиск 🔎'))
