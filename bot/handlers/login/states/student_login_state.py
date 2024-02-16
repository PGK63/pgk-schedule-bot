from aiogram.dispatcher.filters.state import StatesGroup, State


class StudentLoginState(StatesGroup):
    InputDepartment = State()
    InputGroup = State()
