import os
import re
import requests
import time
from datetime import datetime
import pdfplumber
import schedule
import tabula
from psycopg2._json import Json
import locale

from database.common.BaseModel import db
from database.schedule.schedule_datastore import create_schedule
from database.user.user_datastore import get_teachers_by_dep_id, get_students_by_dep_id


def download_and_process_file(url, destination_folder, department_id):
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

        if os.path.exists(new_filename):
            os.remove(new_filename)

        os.rename(filename, new_filename)

        print(f"Файл успешно скачан и переименован как {new_filename}")
        date = convert_to_datetime(extract_date_from_second_row(new_filename))
        print(f"Успешно извлечена дата: {date}")
        json_data = pdf_to_json(new_filename)
        create_schedule(Json(json_data), department_id, date)
        print(f"Файл успешно преобразован в json")

        os.remove(new_filename)
        print(f"Скачанный файл {new_filename} успешно удален.")
        __users_send_message(department_id)
    else:
        print("Не удалось скачать файл.")


def schedule_download(urls, destination_folder, time_of_day, department_ids):
    for url, department_id in zip(urls, department_ids):
        schedule.every().day.at(time_of_day).do(download_and_process_file, url=url,
                                                destination_folder=destination_folder, department_id=department_id)
        print(f"Скачивание по расписанию установлено на {time_of_day} для файла {url} и department_id {department_id}")

    while True:
        schedule.run_pending()
        time.sleep(10)


def pdf_to_json(path: str):
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

                time_value = str(item[number_index + 3])
                if time_value == 'nan':
                    time_value = "1 смена"

                data.append({
                    'group_name': group_name,
                    'number': str(item[number_index]),
                    'teacher': str(item[number_index + 1]),
                    'subject': str(item[number_index + 2]),
                    'time': time_value,
                    'cabinet': str(item[number_index + 4])
                })

    return data


def extract_date_from_second_row(pdf_path: str) -> str:
    date_regex = r'«(\d{1,2})»\s(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s20\d{2}'
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        second_row_text = first_page.extract_text().split('\n')[1]
        match = re.search(date_regex, second_row_text)
        if match:
            extracted_date_str = match.group(0).replace('«', '').replace('»', '')
            return extracted_date_str
        else:
            return None


def convert_to_datetime(date_str):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    day, month_name, year = date_str.split()
    month_number = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }[month_name]
    date_obj = datetime(int(year), month_number, int(day))
    return date_obj


def __users_send_message(department_id):
    text = 'Появилось новое расписание 🕘'
    url = f'https://api.telegram.org/bot5884965201:AAFiqkenkv-xVTf7GyzUu9sfwGFt5RumUtE/sendMessage?text={text}'
    teachers = get_teachers_by_dep_id(department_id)
    students = get_students_by_dep_id(department_id)

    for teacher in teachers:
        requests.post(f'{url}&chat_id={teacher.user_id.chat_id}')

    for student in students:
        requests.post(f'{url}&chat_id={student.user_id.chat_id}')


def main():
    urls = [
        "https://pgk63.ru/assets/files/schedule/itz.pdf",
        "https://pgk63.ru/assets/files/schedule/uz.pdf",
        "https://pgk63.ru/assets/files/schedule/ptz.pdf",
        "https://pgk63.ru/assets/files/schedule/pz.pdf",
        "https://pgk63.ru/assets/files/schedule/gz.pdf"
    ]
    destination_folder = ""
    time_of_day = "15:07"
    department_ids = [1, 2, 3, 4, 5]
    db.connect()
    schedule_download(urls, destination_folder, time_of_day, department_ids)


if __name__ == "__main__":
    main()
