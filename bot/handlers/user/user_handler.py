from aiogram import types, Dispatcher

from database.user.user_datastore import get_role_by_chat_id, get_student_by_chat_id, get_teacher_by_chat_id


async def user_info(message: types.Message):
    role_response = get_role_by_chat_id(message.chat.id)
    if role_response.status_code == 200:
        role = role_response.text.replace('"', "")
        if role == 'STUDENT':
            student = get_student_by_chat_id(message.chat.id).json()
            await message.answer(f'Студент 👨‍🎓\n\n'
                                 f'Группа: {student["groupName"]}\n'
                                 f'Отделения: {student["department"]["name"]}')
        elif role == 'TEACHER':
            teacher = get_teacher_by_chat_id(message.chat.id).json()
            cabinet = ''
            if teacher['cabinet']:
                cabinet = f'Кабинет: {teacher["cabinet"]}\n'
            await message.answer('Преподаватель 👨‍🏫\n\n'
                                 f'Имя: {teacher["firstName"]}\n'
                                 f'Фамилия: {teacher["lastName"]}\n'
                                 f'{cabinet}'
                                 f'Отделения: {teacher["department"]["name"]}')
    else:
        await message.answer('Необходимо зарегистрироваться', disable_notification=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_info, commands="profile")
