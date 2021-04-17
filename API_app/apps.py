import os

from django.apps import AppConfig
from django.conf import settings

import logging

logger = logging.getLogger(__name__)


class ApiAppConfig(AppConfig):
    name = "API_app"
    verbose_name = "Принтеры и чеки"

    def ready(self):
        if not os.path.isdir(settings.MEDIA_ROOT):
            split_MEDIA_ROOT = settings.MEDIA_ROOT.split("/")
            os.mkdir("/".join(split_MEDIA_ROOT[0:-2]))
            os.mkdir("/".join(split_MEDIA_ROOT))

        try:
            from django.contrib.auth.models import User
            from .service.scheduler_task import start_schedule
            from dotenv import load_dotenv

            load_dotenv()
            # Запуск schedule
            start_schedule()
            # Создание администратора, если нет ни одного
            if not User.objects.all().exists():
                User.objects.create_superuser(
                    os.environ.get("ADMIN_NAME", "name_admin"),
                    os.environ.get("ADMIN_EMAIL", "email_admin@admin.admin"),
                    os.environ.get("ADMIN_PASSWORD", "password_admin"),
                )
        except Exception as exc:
            logger.error(
                f"\nЗапуск приложения без базы данных и миграции\nОшибка: {exc}"
            )
