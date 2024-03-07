from aiogram.dispatcher.filters.state import StatesGroup, State


class TeacherLoginState(StatesGroup):
    InputFirstName = State()
    InputLastName = State()
    InputCabinet = State()
    InputDepartment = State()
