from aiogram.dispatcher.filters.state import StatesGroup, State


class TeacherLoginState(StatesGroup):
    InputName = State()
