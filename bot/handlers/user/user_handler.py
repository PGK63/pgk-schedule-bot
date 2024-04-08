from aiogram import types, Dispatcher

from database.user.user_datastore import get_user_by_c_id


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
                                 disable_notification=True)
        elif role == 'TEACHER':
            teacher = json['teacher']
            cabinet = ''

            try:
                cabinet = f'Кабинет: {teacher["cabinet"]}\n'
            except Exception:
                pass

            await message.answer('Преподаватель 👨‍🏫\n\n'
                                 f'Имя: {teacher["firstName"]}\n'
                                 f'Фамилия: {teacher["lastName"]}\n'
                                 f'{cabinet}'
                                 f'Отделения: {teacher["department"]["name"]}',
                                 disable_notification=True)
    else:
        await message.answer('Необходимо зарегистрироваться', disable_notification=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_info, commands="profile")
