def transform_date(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    year, month, day = date.split('-')
    return f'{day} {months[int(month) - 1]} {year} года'
