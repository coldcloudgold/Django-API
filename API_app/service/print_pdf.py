"""Модуль для печати файлов из pdf шаблонов.

Функции
-------
printing(printers: Printer) -> None
    печает файл по шаблону
"""

from API_app.models import Printer

from .business_views import get_checks


def printing(printers: Printer) -> None:
    """Функция для выполнения печати pdf файлов.

    Параметры
    ---------
    printers: Printer
        Список всех доступных принтеров
    """
    for printer in printers:
        checks = get_checks(printer_id=printer, status="rendered")
        if checks:
            for check in checks:
                # TODO: Печать
                print(f"Start printing: check:{check.id}, status:{check.status}")
                check.update_status = "printed"
                print(f"End printing:   check:{check.id}, status:{check.status}")
