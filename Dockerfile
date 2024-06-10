FROM python:3.12

ARG PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN pip install --upgrade pip && apt-get update && apt-get install -y vim

COPY . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
