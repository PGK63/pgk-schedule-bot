from aiogram.dispatcher.filters.state import StatesGroup, State


class StudentScheduleSearchState(StatesGroup):
    StartSearch = State()
