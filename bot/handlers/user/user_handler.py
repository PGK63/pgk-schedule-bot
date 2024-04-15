from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from database.user.user_datastore import get_user_by_c_id, get_secret_key

secret_key_callback = CallbackData('secret_key_callback', 'type')


async def user_info(message: types.Message):
    response = get_user_by_c_id(message.chat.id)
    if response.status_code == 200:
        json = response.json()
        role = json['role']
        if role == 'STUDENT':
            student = json['student']
            await message.answer(f'Студент 👨‍🎓\n\n'
                                 f'Группа: {student["groupName"]}\n'
                                 f'Отделения: {student["department"]["name"]}',
                                 disable_notification=True,
                                 reply_markup=get_secret_keys_reply_markup())
        elif role == 'TEACHER':
            teacher = json['teacher']
            cabinet = ''

            if teacher["cabinet"] is not None:
                cabinet = f'Кабинет: {teacher["cabinet"]}\n'

            await message.answer('Преподаватель 👨‍🏫\n\n'
                                 f'Имя: {teacher["firstName"]}\n'
                                 f'Фамилия: {teacher["lastName"]}\n'
                                 f'{cabinet}'
                                 f'Отделения: {get_departments_text(teacher["departments"])}',
                                 disable_notification=True, reply_markup=get_secret_keys_reply_markup())
    else:
        await message.answer('Необходимо зарегистрироваться', disable_notification=True)


def get_departments_text(departments):
    departments_text = ''
    for i, department in enumerate(departments):
        departments_text += department['name']
        if i < len(departments) - 1:
            departments_text += ', '
    return departments_text


async def secret_key_message(call: types.CallbackQuery, callback_data: dict):
    key_type = callback_data['type']
    key = get_secret_key(call.message.chat.id, key_type)
    key_json = key.json()

    if key.status_code != 200:
        await call.message.answer(key_json['message'], disable_notification=True)
        return

    if key_type == 'ALICE_LOGIN':
        message = f'🔑 Код для входа <i><b><u>{key_json["key"]}</u></b></i>'
        await call.message.answer(message, disable_notification=True)


def get_secret_keys_reply_markup():
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🤖Алиса', callback_data=secret_key_callback.new(type='ALICE_LOGIN')),
            ]
        ]
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_info, commands="profile")
    dp.register_callback_query_handler(secret_key_message, secret_key_callback.filter())
