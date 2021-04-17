import json

from django.http import HttpResponse, JsonResponse
from .models import Check

from django.views.decorators.csrf import csrf_exempt
from .service.business_views import *
from .service.create_pdf import *


def check_admin(request, file_name):
    file = get_file(str(file_name))
    if not file:
        return JsonResponse(
            {"error": "Для данного чека не сгенерирован PDF-файл"}, status=400
        )

    response = HttpResponse(file, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename={os.path.basename(file)}"
    response.status_code = 200
    return response


@csrf_exempt
def create_checks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except:
            return JsonResponse(
                {"error": "Заказ имеет не корректную структуру"}, status=400
            )

        printers = get_printers(point_id=data["point_id"])
        if not printers:
            return JsonResponse(
                {"error": "Для данной точки не настроено ни одного принтера"},
                status=400,
            )

        check = get_check(order=data)
        if check:
            return JsonResponse(
                {"error": "Для данного заказа уже созданы чеки"}, status=400
            )

        for printer in printers:
            # Создание нового чека
            new_check = Check.objects.create(
                printer_id=printer, type=printer.check_type, order=data
            )
            # Создание новой задачи
            new_job = create_pdf.delay(new_check)
        return JsonResponse({"ok": "Чеки успешно созданы"})

    return JsonResponse({"error": "необходим метод POST"}, status=400)


def new_checks(request):
    api_key = request.GET.get("api_key")

    printer = get_printer(api_key=api_key)
    if not printer:
        return JsonResponse({"error": "Ошибка авторизации"}, status=401)

    checks = get_checks(printer_id=printer, status="rendered", need_id=True)
    return JsonResponse({"checks": checks})


def check(request):
    api_key = request.GET.get("api_key")
    check_id = request.GET.get("check_id")

    printer = get_printer(api_key=api_key)
    if not printer:
        return JsonResponse({"error": "Ошибка авторизации"}, status=401)

    check = get_check(pk=check_id)
    if not check:
        return JsonResponse({"error": "Данного чека не существует"}, status=400)

    if check.printer_id != printer:
        return JsonResponse({"error": "Данного чека не существует"}, status=400)

    file = get_file(str(check.pdf_file))
    if not file:
        return JsonResponse(
            {"error": "Для данного чека не сгенерирован PDF-файл"}, status=400
        )

    response = HttpResponse(file, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename={os.path.basename(file)}"
    response.status_code = 200
    return response
