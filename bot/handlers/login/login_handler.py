import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.handlers.login.states.student_login_state import StudentLoginState
from bot.handlers.login.states.teacher_login_state import TeacherLoginState
from database.department.department_datastore import get_departments
from database.user.user_datastore import create_student, create_teacher, delete_user_by_chat_id, \
    user_exist

user_role_callback = CallbackData('user_role_callback', 'role')
department_callback = CallbackData('department_callback', 'id', 'user_role')
sign_out_callback = CallbackData('sign_out_callback')

sticker_hello_id = 'CAACAgIAAxkBAAELbFZl0Jiomdm00O5xdLWWiTkH9WnAQwACxgEAAhZCawpKI9T0ydt5RzQE'
sticker_ok_id = 'CAACAgIAAxkBAAELbFpl0JlB7s_u0DV0-IY2PzdY-ZpXbAACogEAAhZCawqhd3djmk6DITQE'


async def login(message: types.Message):
    user = user_exist(message.chat.id)

    if not user:
        await message.answer_sticker(sticker_hello_id, disable_notification=True)
        await message.answer(
            text="Вы студент или преподаватель?",
            disable_notification=True,
            reply_markup=types.InlineKeyboardMarkup(
                row_width=1,
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text='Студент 👨‍🎓',
                            callback_data=user_role_callback.new(role='student')
                        ),
                        types.InlineKeyboardButton(
                            text='Преподаватель 👨‍🏫',
                            callback_data=user_role_callback.new(role='teacher')
                        )
                    ]
                ]
            )
        )
    else:
        await message.answer(
            'Необходимо выйти из учетной записи',
            disable_notification=True,
            reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                [
                    InlineKeyboardButton('Выйти', callback_data=sign_out_callback.new())
                ]
            ])
        )


async def role_callback(call: types.CallbackQuery, callback_data: dict):
    role = callback_data.get('role')
    if role == 'teacher':
        await call.message.answer('🖍 Введите имя', disable_notification=True)
        await TeacherLoginState.InputFirstName.set()
    elif role == 'student':
        await call.message.answer('🏫 Выберите отделение', disable_notification=True,
                                  reply_markup=get_departments_reply_markup('student'))
        await StudentLoginState.InputDepartment.set()


async def teacher_input_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await message.answer('🖍 Введите фамилию', disable_notification=True)
    await state.update_data(first_name=first_name)
    await TeacherLoginState.next()


async def teacher_input_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await message.answer('🏫 Напишите свой кабинет в формате 301/4 или выберите из списка', disable_notification=True,
                         reply_markup=ReplyKeyboardMarkup(
                             one_time_keyboard=True,
                             resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton("Физ-ра"),
                                     KeyboardButton("Кр.пол")
                                 ],
                                 [

                                     KeyboardButton("У меня нет кабинета")
                                 ]
                             ]))
    await state.update_data(last_name=last_name)
    await TeacherLoginState.next()


async def teacher_input_cabinet(message: types.Message, state: FSMContext):
    cabinet = message.text
    if cabinet == 'У меня нет кабинета':
        cabinet = None

    await message.answer('🏫 Выберите отделение', disable_notification=True,
                         reply_markup=get_departments_reply_markup('teacher'))
    await state.update_data(cabinet=cabinet)
    await TeacherLoginState.next()


async def teacher_input_department(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    state_data = await state.get_data()

    department_id = callback_data.get('id')
    last_name = state_data.get('last_name')
    first_name = state_data.get('first_name')
    cabinet = None

    try:
        cabinet = state_data.get('cabinet')
    except Exception:
        pass

    create_teacher(call.message.chat.id, first_name, last_name, department_id, cabinet)
    await state.finish()
    await call.message.answer_sticker(sticker_ok_id, disable_notification=True, reply_markup=get_default_reply_markup())


async def student_input_department(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    department_id = callback_data.get('id')
    user_role = callback_data.get('user_role')

    await call.message.answer('🏫 Отправьте название группы в формате примера\nПример: ИСП-34',
                              disable_notification=True)
    await state.update_data(department_id=department_id, user_role=user_role)
    await StudentLoginState.next()


async def student_input_group(message: types.Message, state: FSMContext):
    group_name = message.text.strip().upper()

    if re.findall("^(([А-Я]{2}|[А-Я]{3})-([0-9]{2}|[0-9]{3}))$", group_name):
        state_data = await state.get_data()
        department_id = state_data.get('department_id')
        create_student(message.chat.id, group_name, department_id)
        await message.answer_sticker(sticker_ok_id, reply_markup=get_default_reply_markup(), disable_notification=True)
        await state.finish()
    else:
        await message.answer('❌ Неверный формат группы')


def get_departments_reply_markup(user_role):
    departments = get_departments()
    departments_inline_keyboard = []

    for department in departments:
        departments_inline_keyboard.append(
            [InlineKeyboardButton(department['name'],
                                  callback_data=department_callback.new(id=department['id'], user_role=user_role))])

    return InlineKeyboardMarkup(row_width=1, inline_keyboard=departments_inline_keyboard)


def get_default_reply_markup():
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1, keyboard=[
        [
            KeyboardButton('Расписание 🕘')
        ],
        [
            KeyboardButton('Расписание звонков 🕘')
        ]
    ])


async def sign_out(call: types.CallbackQuery):
    delete_user_by_chat_id(call.message.chat.id)
    await call.message.answer('Успешно', disable_notification=True, reply_markup=types.ReplyKeyboardRemove())


def register_login(dp: Dispatcher):
    dp.register_message_handler(login, commands=['start'])
    dp.register_callback_query_handler(sign_out, sign_out_callback.filter())

    dp.register_callback_query_handler(role_callback, user_role_callback.filter())
    dp.register_callback_query_handler(student_input_department, department_callback.filter(),
                                       state=StudentLoginState.InputDepartment)

    dp.register_message_handler(student_input_group, state=StudentLoginState.InputGroup)

    dp.register_message_handler(teacher_input_first_name, state=TeacherLoginState.InputFirstName)
    dp.register_message_handler(teacher_input_last_name, state=TeacherLoginState.InputLastName)
    dp.register_message_handler(teacher_input_cabinet, state=TeacherLoginState.InputCabinet)
    dp.register_callback_query_handler(teacher_input_department, department_callback.filter(),
                                       state=TeacherLoginState.InputDepartment)
