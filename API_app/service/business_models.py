"""Модуль для выполнения бизнес логики в models.

Классы
------
ServicePrinter
    переопеределяет функции "clean", "save"
ServiceCheck
    переопеределяет функции "clean", "save", добавляет свойство "update_status"
"""

from django.core.exceptions import ValidationError

import API_app.models


class ServicePrinter:
    """Класс переопределяет стандартные функции "clean", "save" для модели "Printer"."""

    def clean(self):
        if self.point_id < 0:
            raise ValidationError("Проверьте корректность введенной точки")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class ServiceCheck:
    """Класс переопределяет стандартные функции "clean", "save", а также добавляет свойство "update_status" модели "Check"."""

    def clean(self):
        if (
            API_app.models.Check.objects.filter(
                printer_id=self.printer_id,
                type=self.type,
                order=self.order,
                status=self.status,
                pdf_file=self.pdf_file,
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError("Такой чек уже существует")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    @property
    def update_status(self):
        return self.status

    @update_status.setter
    def update_status(self, new_status):
        for choise_status in self.value_choices_status:
            if new_status in choise_status[0]:
                self.status = new_status
                self.save()
