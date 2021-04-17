from django.contrib import admin
from .models import Printer, Check


class PrinterAdmin(admin.ModelAdmin):
    class Meta:
        model = Printer

    list_display = ("name", "check_type", "point_id")
    list_display_links = ("name",)
    search_fields = ("name", "check_type", "point_id")
    list_filter = ("name", "check_type", "point_id")


class CheckAdmin(admin.ModelAdmin):
    class Meta:
        model = Check

    list_display = ("printer_id", "type", "status")
    list_display_links = ("printer_id",)
    search_fields = ("printer_id", "type", "status")
    list_filter = ("printer_id", "type", "status")


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
