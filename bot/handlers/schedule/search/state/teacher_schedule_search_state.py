from aiogram.dispatcher.filters.state import StatesGroup, State


class TeacherScheduleSearchState(StatesGroup):
    StartSearch = State()
