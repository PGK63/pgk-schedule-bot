import requests

from database.common.constants import BASE_URL, API_TOKEN


def get_teachers(name):
    return requests.get(f'{BASE_URL}/teachers?name={name}', headers={
        'X-API-KEY': API_TOKEN
    }).json()


def teacher_get_fio(teacher):
    fio = teacher['lastName'] + " " + teacher['firstName']
    if teacher['middleName']:
        fio += " " + teacher['middleName']
    return fio
