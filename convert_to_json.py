import re

import tabula


def pdf_to_json(path: str) -> dir:
    data = []

    df = tabula.read_pdf(path, pages="all")

    for index, i in enumerate(df):
        last_group = "-"

        for index, item in enumerate(i.values):
            if index != 0 or index > 0:
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
