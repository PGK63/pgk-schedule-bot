import requests
from database.common.constants import BASE_URL, API_TOKEN


def get_departments():
    response = requests.get(f"{BASE_URL}/departments", headers={
        'X-API-KEY': API_TOKEN
    })
    if response.status_code == 200:
        return response.json()
    return None
