import requests
from datetime import datetime

from database.common.constants import BASE_URL


def get_schedules_by_dep_id(department_id):
    response = requests.get(f"{BASE_URL}/schedules?departmentId={department_id}")
    if response.status_code == 200:
        return response.json()
    return None


def student_get_schedules_message(chat_id, schedule_id) -> str:
    response = requests.get(f'{BASE_URL}/schedules/{schedule_id}/student/by-telegram-id/{chat_id}')
    json = response.json()

    if response.status_code != 200:
        return json['message']

    date = datetime.strptime(json['date'], '%Y-%m-%d').date()
    date = date.strftime('%a, %d %B %Y').capitalize()
    message = f"<i><b><u>{date} ({json['shift']})</u></b></i>\n\n"

    for column in json['columns']:
        teacher = column['teacher']
        cabinet = column['cabinet']
        number = f"🕒 Пара: {column['number']}"
        if not teacher:
            teacher = "Не указан"
        if not cabinet:
            cabinet = "Не указан"

        if bool(column['exam']):
            number += f" (📌Экзамен)"

        message += (f"{number}\n"
                    f"🏢 Кабинет: {cabinet}\n"
                    f"👤 {teacher}\n"
                    f"\n")

    return message


def teacher_get_schedules_message(chat_id, schedule_id) -> str:
    response = requests.get(f'{BASE_URL}/schedules/{schedule_id}/teacher/by-telegram-id/{chat_id}')
    json = response.json()

    if response.status_code != 200:
        return json['message']

    date = datetime.strptime(json['date'], '%Y-%m-%d').date()
    date = date.strftime('%a, %d %B %Y').capitalize()
    message = f"<i><b><u>{date}</u></b></i>\n\n"

    for column in json['columns']:
        exam = ''
        if bool(column['exam']):
            exam = f"\n📌 Экзамен"

        message += (f"🕒 Пара: {column['number']} ({column['shift']})\n"
                    f"🏢 Кабинет: {column['cabinet']}\n"
                    f"👥 Группа: {column['group_name']}"
                    f"{exam}"
                    f"\n\n")

    return message
