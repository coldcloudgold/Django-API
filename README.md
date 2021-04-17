# API

## Суть проекта:

Необходимость в реализации сервиса для получения и дальнешей обработки заказов.

## Стек:

1. База данных: **PostgreSQL**.

2. Фреймворк: **Django**.

3. Очередь (+ задача с периодическим выполнением): **Redis** (django-rq; rq-schedule).

4. WSGI: **Gunicorn**.

5. Веб-сервер: **Nginx**.

6. Развертывание: **Docker-Compose**. 

## Пример работы API:

### Создание чеков для заказа (create_checks):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/API/Create_check.gif)

### Список доступных чеков для печати (create_checks):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/API/New_checks.gif)

### PDF-файл чека (check):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/API/Check.gif)

## Административное управление сервисом:

Сервис предоставляет удобную административную панель, в которой можно как отслеживать за ходом выполнения работы сервиса (Redis Queue), так и совершать различные манипуляции с принтерами и чеками. 

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/API/Admin_API.gif)

## Запуск проекта:

1. Изменить название *example.env* на *.env*, при необходимости внеся в него коррективы.

2. Убедиться, что необходимые порты для работы проекта не заняты (8080 - nginx, 5433 - postgres, 6380 - redis, 8001 - django/gunicorn, 8081 - wkhtmltopdfaas):

`sudo netstat -tulpn | grep :<xxxx>`

где `xxxx` - номер порта.

3. Если на данных портах запущены стандартные сервисы, их необходимо выключить:

```
sudo kill `sudo lsof -t -i:<xxxx>`
```

4. Создать docker-compose:

`docker-compose build`

5. Запустить docker-compose:

`docker-compose up -d`

Примерно через 30 секунд сервис станет пригодным для использования.

6. Остановить и удалить docker-compose:

`docker-compose down -v ; sudo rm -r media/ static/ API_app/migrations/0001_initial.py ./<logging_name.log>`

где `<logging_name.log>` - имя логера (по умолчанию: `logging.log`).


## Методы:

Доступные методы находятся в файле **api.yml**. Отрендерить: [swagger](https://editor.swagger.io/)


## Полезное:

### Зайти в панель администратора (пользователь создается по умолчанию), если не менялись соотетствующие параметры в окружении:

```
Name: name_admin
Email: email_admin@admin.admin
Password: password_admin
```

### Зайти в контейнер:

1. Просмотреть список всех работающих контейнеров:

`docker ps`

2. Зайти в необходимый контейнер по его имени или id (например, redis): 

```
docker exec -it <redis_container> <***> 
redis-cli
```

где `<***>` - оболочка (в образах основанных на alpine - `sh`, ubuntu - `bash`).
