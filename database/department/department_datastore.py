import requests
from database.common.constants import BASE_URL


def get_departments():
    response = requests.get(f"{BASE_URL}/departments")
    if response.status_code == 200:
        return response.json()
    return None
