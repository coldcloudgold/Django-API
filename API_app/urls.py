from django.urls import path
from . import views


urlpatterns = [
    path("create_checks/", views.create_checks),
    path("new_checks/", views.new_checks),
    path("check/", views.check),

    # ADMIN
    path("media/pdf/<file_name>", views.check_admin),
]
