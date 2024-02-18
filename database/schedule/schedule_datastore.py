import ast

from database.schedule.model.schedule_entity import ScheduleEntity


def create_schedule(json, department_id, date):
    ScheduleEntity.create(json=json, department_id=department_id, date=date)


def get_schedules_by_dep_id(department_id):
    return ScheduleEntity.select().where(ScheduleEntity.department_id == department_id)


def get_schedule_by_id(schedule_id) -> ScheduleEntity:
    return ScheduleEntity.get(ScheduleEntity.id == schedule_id)


def student_get_schedules_message(group_name, schedule_id) -> (str, str):
    message = ''
    unknown_message = ''
    schedule = get_schedule_by_id(schedule_id)
    schedule_json = ast.literal_eval(str(schedule.json))

    for item in schedule_json:
        if item['group_name'] == group_name:
            message += __get_schedule_message(item)
        elif item['group_name'] == '-':
            unknown_message += __get_schedule_message(item)

    return message, unknown_message


def teacher_get_schedules_message(first_name, last_name, schedule_id) -> (str, str):
    message = ''
    unknown_message = ''
    schedule = get_schedule_by_id(schedule_id)
    schedule_json = ast.literal_eval(str(schedule.json))

    for item in schedule_json:
        if f'{last_name} {first_name.strip().upper()[0]}.' in item['teacher']:
            message += __get_schedule_message(item)

        if item['group_name'] == '-':
            unknown_message += __get_schedule_message(item)

    return message, unknown_message


def __get_schedule_message(schedule) -> str:
    return (f"<i><b><u>{schedule['time']}</u></b></i>\n"
            f"🕒 Пара: {schedule['number']}\n"
            f"🏢 Кабинет: {schedule['cabinet']}\n"
            f"🎓 Предмет: {schedule['subject']}\n"
            f"👤 Преподаватель: {schedule['teacher']}\n"
            f"👥 Группа: {schedule['group_name']}"
            f"\n\n")
