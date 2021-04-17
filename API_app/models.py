from django.db import models

from .service.business_models import *


class Printer(ServicePrinter, models.Model):
    """Класс для принтера

    Поля
    ----
    name: CharField
        Название принтера
    api_key: CharField
        Уникальный ключ доступа
    check_type: CharField
        Тип принтера (kitchen/client)
    point_id: IntegerField
        Точка, к которой привязан принтер

    Возвращает
    ----------
    str: str
        Имя, тип чека, точка
    """

    name = models.CharField(max_length=100, verbose_name="Принтер")
    api_key = models.CharField(max_length=250, unique=True, verbose_name="Ключ")
    value_choices_type = [
        ("kitchen", "kitchen"),
        ("client", "client"),
    ]
    check_type = models.CharField(
        max_length=7, choices=value_choices_type, verbose_name="Тип чека"
    )
    point_id = models.IntegerField(verbose_name="Точка (принтера)")

    def __str__(self):
        return f"{self.name}, {self.check_type}, {self.point_id}"

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"
        ordering = ["point_id"]


class Check(ServiceCheck, models.Model):
    """Класс для чека

    Поля
    ----
    printer_id: ForeignKey
        Номер принтера, на котором печатается чек
    type: CharField
        Тип чека (kitchen/client)
    order: JSONField
        Заказ в формате JSON
    status: CharField
        Тип принтера (new/rendered/printed)
    point_id: IntegerField
        Точка, к которой привязан принтер
    pdf_file:
        Название сгенерированного PDF файла

    Возвращает
    ----------
    str: str
        Номер принтера, тип чека, статус, имя PDF файла
    """

    printer_id = models.ForeignKey(
        to=Printer,
        on_delete=models.CASCADE,
        related_name="from_printer_set",
        verbose_name="Привязанный принтер",
    )
    value_choices_type = [
        ("kitchen", "kitchen"),
        ("client", "client"),
    ]
    type = models.CharField(
        max_length=7, choices=value_choices_type, verbose_name="Тип чека"
    )
    order = models.JSONField(default=dict, verbose_name="JSON")
    value_choices_status = [
        ("new", "new"),
        ("rendered", "rendered"),
        ("printed", "printed"),
    ]
    status = models.CharField(
        max_length=8,
        default=value_choices_status[0][0],
        null=True,
        choices=value_choices_status,
        verbose_name="Статус чека",
    )
    pdf_file = models.FileField(verbose_name="Файл pdf", null=True, blank=True)

    def __str__(self):
        return f"{self.printer_id}, {self.type}, {self.status}, {self.pdf_file}"

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
        ordering = ["printer_id"]
