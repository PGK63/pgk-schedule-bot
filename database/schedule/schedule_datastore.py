import requests
from datetime import datetime

from database.common.constants import BASE_URL, API_TOKEN


def department_id_to_str(department_ids):
    return ','.join(str(dep['id']) for dep in department_ids)


def get_schedules_by_dep_id_str(department_id_str, page):
    url = f"{BASE_URL}/schedules?"
    for dep_id in department_id_str:
        url += f"departmentIds={dep_id}&"
    url += f"offset={page}"

    response = requests.get(url, headers={
        'X-API-KEY': API_TOKEN
    })

    if response.status_code == 200:
        return response.json()
    return None


def get_schedules_by_dep_id(department_id, page):
    return get_schedules_by_dep_id_str(department_id_to_str(department_id), page)


def get_schedules_by_teacher_id(teacher_id, page):
    url = f"{BASE_URL}/schedules/by-teacher-id/{teacher_id}?offset={page}"
    response = requests.get(url, headers={
        'X-API-KEY': API_TOKEN
    })

    if response.status_code == 200:
        return response.json()
    return None


def student_get_schedules_message(chat_id, schedule_id) -> str:
    response = requests.get(f'{BASE_URL}/schedules/{schedule_id}/student/by-telegram-id/{chat_id}', headers={
        'X-API-KEY': API_TOKEN
    })
    json = response.json()

    if response.status_code != 200:
        return json['message']

    if len(json['columns']) == 0:
        return "Пар нет 🎉"

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


def teacher_get_schedules_message_by_teacher_id(schedule_id, teacher_id) -> str:
    response = requests.get(f'{BASE_URL}/schedules/{schedule_id}/teacher/{teacher_id}', headers={
        'X-API-KEY': API_TOKEN
    })
    return teacher_get_schedules_message(response.json(), response.status_code)


def teacher_get_schedules_message_chat_id(chat_id, schedule_id) -> str:
    response = requests.get(f'{BASE_URL}/schedules/{schedule_id}/teacher/by-telegram-id/{chat_id}', headers={
        'X-API-KEY': API_TOKEN
    })
    return teacher_get_schedules_message(response.json(), response.status_code)


def teacher_get_schedules_message(json, status_code) -> str:
    if status_code != 200:
        return json['message']

    if len(json['rows']) == 0:
        return "Пар нет 🎉"

    date = datetime.strptime(json['date'], '%Y-%m-%d').date()
    date = date.strftime('%a, %d %B %Y').capitalize()
    message = f"<i><b><u>{date}</u></b></i>\n"

    for row in json['rows']:
        message += f"\n👥 <b>{row['group_name']} ({row['shift']})</b>\n"

        for column in row['columns']:
            exam = ''
            if bool(column['exam']):
                exam = f"\n📌 Экзамен"

            message += (f"🕒 Пара: {column['number']}\n"
                        f"🏢 Кабинет: {column['cabinet']}\n"
                        f"{exam}")

    return message
