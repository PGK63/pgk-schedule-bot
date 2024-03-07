import requests

from database.common.constants import BASE_URL


def get_user_by_chat_id(c_id):
    response = requests.get(f"{BASE_URL}/students/by-telegram-id/{c_id}")
    if response.status_code == 200:
        return response.json()
    return None


def get_student_by_id(user_id):
    response = requests.get(f"{BASE_URL}/students/by-telegram-id/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None


def get_teacher_by_id(user_id):
    response = requests.get(f"{BASE_URL}/teachers/by-telegram-id/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None


def create_student(chat_id, group, department_id):
    student_data = {
        "groupName": group,
        "departmentId": department_id,
    }
    response = requests.post(f"{BASE_URL}/students/telegram/{chat_id}", json=student_data)
    if response.status_code == 201:
        return response.json()
    return None


def create_teacher(chat_id, first_name, last_name, department_id, cabinet):
    user_data = {
        "firstName": first_name,
        "lastName": last_name,
        "cabinet": cabinet,
        "departmentId": department_id
    }
    response = requests.post(f"{BASE_URL}/teachers/telegram/{chat_id}", json=user_data)
    if response.status_code == 201:
        return response.json()
    return None


def delete_user_by_chat_id(c_id):
    requests.delete(f"{BASE_URL}/users/by-telegram-id/{c_id}")

