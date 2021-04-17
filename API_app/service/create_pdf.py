"""Модуль для создания задач и генерации pdf файлов.

Функции
-------
create_pdf(new_check: Check) -> None
    задача в RedisQueue, создающая pdf файл
"""

import os
import logging
import base64
import json
from typing import Any

import requests

from django.template import Context, Template
from django.core.files.base import File
from API_app.models import Check

from django_rq import job

from django.conf import settings

logger = logging.getLogger(__name__)


@job
def create_pdf(new_check: Check) -> Any:
    """Функция генерирует pdf файл.

    Параметры
    ---------
    new_check: Check
        Инстанс класса "Check"

    Возвращает
    ----------
    Any: str
        Если генерация pdf файла прошла успешно, возращается соответствующая строка
    Any: str
        Если генерация pdf файла прошла не успешно, возращается соответствующая строка, ведется запись в лог
    """
    url = f"http://{settings.HTMLTOPDF_ADDRES}:{settings.HTMLTOPDF_PORT}"

    if new_check.type == "kitchen":
        file_name = "kitchen_check.html"
        name_postfix = "kitchen"
    else:
        file_name = "client_check.html"
        name_postfix = "client"

    file = os.path.join(settings.TEMPLATES[0]["DIRS"][0], file_name)

    with open(file, mode="r") as f:
        temlate = Template(template_string=f.read())

    context = Context({"check": new_check.order})
    rendered_template = temlate.render(context)
    contents = base64.b64encode(rendered_template.encode()).decode("utf-8")
    data = {"contents": contents}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        output_file_name = f'{new_check.order["id"]}_{name_postfix}'
        output_file_path = f"{settings.MEDIA_ROOT}{output_file_name}_del.pdf"

        with open(output_file_path, "wb") as f:
            f.write(response.content)

        with open(output_file_path, mode="rb") as f:
            new_check.pdf_file.save(f"{output_file_name}.pdf", File(f))

        new_check.update_status = "rendered"
        os.remove(output_file_path)

        return f'Обработано\nЧек: {new_check.pk};\nЗаказ: {new_check.order["id"]}'

    except Exception as exc:
        logger.error(
            f'\nНе обработано\nЧек: {new_check.pk}\nЗаказ: {new_check.order["id"]}\nОшибка: {exc}'
        )
        return f'Не обработано\nЧек: {new_check.pk}\nЗаказ: {new_check.order["id"]}\nОшибка: {exc}'
