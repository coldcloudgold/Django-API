"""Модуль для выполнения бизнес логики во views.

Функции
-------
get_file(file_name: str) -> Any
    возвращает файл или ничего ("None")
get_printer(api_key: str) -> Printer
    возвращает принтер
get_printers(point_id: str) -> list
    возвращает принтеры
get_check(pk: str = None, order: json = None) -> Check
    возвращает чек
get_checks(printer_id: Printer, status: str, need_id: bool = False) -> Any
    возвращает список (из "id") чеков
"""

import os
import json
from typing import Any

from API_app.models import Printer, Check

from django.conf import settings


def get_file(file_name: str) -> Any:
    """Функция возвращает файл или ничего "None".

    Параметры
    ---------
    file_name: str
        Имя pdf файла

    Возвращает
    ----------
    Any: bytes
        Байты считанного файла (если такой файл существует)
    Any: None
        Ничего (если такого файла не существует)
    """
    file = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.isfile(file):
        with open(file, "rb") as f:
            readed_file = f.read()
    else:
        readed_file = None
    return readed_file


def get_printer(api_key: str) -> Printer:
    """Функция возвращает принтер.

    Параметры
    ---------
    api_key: str
        Уникальный ключ доступа к принтеру

    Возвращает
    ----------
    Any: printer
        Притер (если задан "api_key")
    """
    printer = Printer.objects.filter(api_key=api_key).first()
    return printer


def get_printers(point_id: str) -> list:
    """Функция возвращает принтеры.

    Параметры
    ---------
    point_id: str
        Номер точки, к которой привязан принтер

    Возвращает
    ----------
    Any: list Printer's
        Список принтеров
    """
    printers = Printer.objects.filter(point_id=point_id)
    return printers


def get_check(pk: str = None, order: json = None) -> Check:
    """Функция возвращает чек.

    Параметры
    ---------
    pk: str
        Уникальный идентификатор чека
    order: json
        Информация о заказе

    Возвращает
    ----------
    Any: Check
        Чек
    """
    if pk != None:
        check = Check.objects.filter(pk=pk).first()
    else:
        check = Check.objects.filter(order=order).first()
    return check


def get_checks(printer_id: Printer, status: str, need_id: bool = False) -> Any:
    """Функция возвращает список (из "id") чеков.

    Параметры
    ---------
    printer_id: Printer
        Номер принтера, к которому привязан чек
    status: str
        Статус выполнение заказа (new/rendered/printed)
    need_id: bool
        Указывает, нужны ли только "id" (True/False)

    Возвращает
    ----------
    Any: list Check's
        Список чеков
    Any: list "id" Check's
        Список "id" чеков, если "need_id" переключен в "True"
    """
    if need_id == True:
        checks = list(
            Check.objects.values("id").filter(printer_id=printer_id, status=status)
        )
    else:
        checks = Check.objects.filter(printer_id=printer_id, status=status)
    return checks
