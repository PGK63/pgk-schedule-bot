FROM python:3.10

# Установка пакетов для русской локали и генерация локали
RUN apt-get update && apt-get install -y locales && \
    sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

# Установка переменных окружения для русской локали
ENV LANG ru_RU.UTF-8  
ENV LANGUAGE ru_RU:en  
ENV LC_ALL ru_RU.UTF-8

# Копирование приложения в рабочий каталог
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
COPY . .

# Запуск приложения
CMD ["python3", "bot.py"]
