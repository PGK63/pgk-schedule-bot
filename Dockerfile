FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .
CMD ["python3", "bot.py", "&&", "python3", "download_file.py"]