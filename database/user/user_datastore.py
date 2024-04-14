import requests

from database.common.constants import BASE_URL, API_TOKEN


def get_user_by_c_id(chat_id):
    return requests.get(f"{BASE_URL}/users/by-telegram-id/{chat_id}", headers={
        'X-API-KEY': API_TOKEN
    })


def user_exist(c_id):
    return get_user_by_c_id(c_id).status_code == 200


def create_student(chat_id, group, department_id):
    student_data = {
        "groupName": group,
        "departmentId": department_id,
    }
    response = requests.post(f"{BASE_URL}/students/telegram/{chat_id}", json=student_data, headers={
        'X-API-KEY': API_TOKEN
    })
    if response.status_code == 201:
        return response.json()
    return None


def create_teacher(chat_id, teacher_id):
    response = requests.post(f"{BASE_URL}/teacher/{teacher_id}/user/by-telegram-id/{chat_id}", headers={
        'X-API-KEY': API_TOKEN
    })
    if response.status_code == 201:
        return response.json()
    return None


def delete_user_by_chat_id(c_id):
    requests.delete(f"{BASE_URL}/users/by-telegram-id/{c_id}", headers={
        'X-API-KEY': API_TOKEN
    })


def get_teacher_by_chat_id(c_id):
    return requests.get(f"{BASE_URL}/teachers/by-telegram-id/{c_id}", headers={
        'X-API-KEY': API_TOKEN
    })


def get_student_by_chat_id(c_id):
    return requests.get(f"{BASE_URL}/students/by-telegram-id/{c_id}", headers={
        'X-API-KEY': API_TOKEN
    })
