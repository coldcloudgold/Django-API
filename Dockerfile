FROM python:3.8-alpine


# обновление
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


# напоминание о порте
EXPOSE 8001


# создание и перемещение в новую директорию
WORKDIR /API


# добавление переменных среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# установка пакетов и копирование точки входа
RUN pip install --upgrade pip
COPY requirements.txt entrypoint.sh ./
RUN pip install -r requirements.txt && chmod +x entrypoint.sh


# копирование проекта
COPY . .


# добавление точки входа
ENTRYPOINT ["/API/entrypoint.sh"]
