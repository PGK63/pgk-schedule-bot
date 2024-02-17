from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bot.common.date import transform_date
from database.schedule.schedule_datastore import get_schedules_by_dep_id, student_get_schedules_message, \
    teacher_get_schedules_message
from database.user.user_datastore import get_user_by_chat_id, get_student_by_id, get_teacher_by_id

schedule_callback = CallbackData('schedule_id_callback', 'id', 'group_name', 'user_role','teacher_first_name',
                                 'teacher_last_name')


async def schedules_message(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)

    if user:
        user_role = user.user_role_id.role
        dep_id = None
        group_name = ''
        teacher_last_name = ''
        teacher_first_name = ''

        if user_role == 'STUDENT':
            student = get_student_by_id(user.id)
            dep_id = student.department_id
            group_name = student.group_name
        elif user_role == 'TEACHER':
            teacher = get_teacher_by_id(user.id)
            dep_id = teacher.department_id
            teacher_last_name = teacher.last_name
            teacher_first_name = teacher.first_name

        schedules = get_schedules_by_dep_id(dep_id)
        schedules_inline_keyboard = []

        for schedule in schedules:
            schedules_inline_keyboard.append([
                InlineKeyboardButton(
                    transform_date(str(schedule.date)),
                    callback_data=schedule_callback.new(id=schedule.id, group_name=group_name, user_role=user_role,
                                                        teacher_last_name=teacher_last_name,
                                                        teacher_first_name=teacher_first_name)
                )
            ])

        await message.answer('Выберите день',
                             reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=schedules_inline_keyboard))


async def schedule_callback_message(call: types.CallbackQuery, callback_data: dict):
    schedule_id = callback_data.get('id')
    user_role = callback_data.get('user_role')
    message = ''

    if user_role == 'STUDENT':
        group_name = callback_data.get('group_name')
        message = student_get_schedules_message(group_name, schedule_id)
    elif user_role == 'TEACHER':
        teacher_first_name = callback_data.get('teacher_first_name')
        teacher_last_name = callback_data.get('teacher_last_name')
        message = teacher_get_schedules_message(teacher_first_name, teacher_last_name, schedule_id)

    if not message:
        message = 'Расписание отсутствует'

    await call.message.answer(message)


def register_schedule(dp: Dispatcher):
    dp.register_message_handler(schedules_message, (lambda message: message.text == 'Расписание 🕘'))
    dp.register_callback_query_handler(schedule_callback_message, schedule_callback.filter())
