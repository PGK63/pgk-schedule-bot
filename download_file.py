import os
import re

import requests
import schedule
import time
from datetime import datetime

import tabula
from psycopg2._json import Json

from database.schedule.schedule_datastore import create_schedule


def download_file(url, destination_folder, department_id):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(destination_folder, url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)

        time.sleep(2)

        if department_id:
            new_filename = os.path.join(destination_folder, f"{department_id}_{url.split('/')[-1]}")
        else:
            new_filename = filename

        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")
        file_extension = os.path.splitext(new_filename)[1]
        new_filename = os.path.join(destination_folder, str(department_id) + "_" + formatted_date + file_extension)

        os.rename(filename, new_filename)

        print(f"Файл успешно скачан и переименован как {new_filename}")
        json = pdf_to_json(new_filename)
        create_schedule(Json(json), department_id, formatted_date)
        print(f"Файл успешно преобразован в json")

    else:
        print("Не удалось скачать файл.")


def schedule_download(url, destination_folder, time_of_day, department_id):
    schedule.every().day.at(time_of_day).do(download_file, url=url, destination_folder=destination_folder,
                                            department_id=department_id)
    print(f"Скачивание по расписанию установлено на {time_of_day}")

    while True:
        schedule.run_pending()
        time.sleep(10)


def pdf_to_json(path: str) -> dir:
    print(path)
    data = []

    df = tabula.io.read_pdf(path, pages="all")

    for inx, i in enumerate(df):
        last_group = "-"

        for index, item in enumerate(i.values):
            print(item)
            if inx != 0 or index > 0:
                number_index = 1

                group_name = str(item[0])

                if re.findall("^(([А-Я]{2}|[А-Я]{3})-([0-9]{2}|[0-9]{3}))$", group_name):
                    last_group = group_name
                else:
                    if re.findall("^[1-9]$", group_name):
                        number_index = 0

                    group_name = last_group

                time = str(item[number_index + 3])
                if time == 'nan':
                    time = "1 смена"

                data.append({
                    'group_name': group_name,
                    'number': str(item[number_index]),
                    'teacher': str(item[number_index + 1]),
                    'subject': str(item[number_index + 2]),
                    'time': time,
                    'cabinet': str(item[number_index + 4])
                })

    return data


if __name__ == "__main__":
    url = "https://pgk63.ru/assets/files/schedule/itz.pdf"
    destination_folder = ""
    time_of_day = "21:43"
    department_id = 1

    schedule_download(url, destination_folder, time_of_day, department_id)
