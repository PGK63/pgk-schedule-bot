from aiogram.dispatcher.filters.state import StatesGroup, State


class TeacherScheduleSearchState(StatesGroup):
    InputSchedule = State()
    InputTeacher = State()
