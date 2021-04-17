"""Модуль для запуска планировщика задач.

Функции
-------
start_schedule() -> None
    запускает планировщика задач
"""

from datetime import datetime

import django_rq

from API_app.models import Printer

from .print_pdf import printing


def start_schedule() -> None:
    """Функция для запуска планировщика задач."""
    scheduler = django_rq.get_scheduler("default")
    for job in scheduler.get_jobs():
        job.delete()
    printers = Printer.objects.all()
    job = scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=printing,
        args=(printers,),
        interval=5,
    )
