import os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from celery.result import AsyncResult

from . import services
from .exceptions import FileNotAllowed, ImageRequired
from .models import CoinResponse, CoinRequest
from .tasks import recognize


@api_view(["GET"])
def api_roots(request):
    base_host = f"http://{request.get_host()}"

    return Response({"recognize": f"{base_host}{reverse('core:recognize')}"})


@csrf_exempt
def recognize_request(request):
    if request.method == "POST":
        print(cache.get("model_cache"))
        image = services.get_image(request)
        new_request = CoinRequest()
        new_request.save()
        new_request.image.save(image.name, image)
        task = recognize.delay(new_request.id)
        new_request.celery_id = task.id
        new_request.save()
        return JsonResponse({"task_id": task.id}, status=202)
    else:
        return JsonResponse({"error": "Not allowed method"})


@csrf_exempt
def recognize_response(request, task_id):
    celery_result = AsyncResult(task_id)
    if celery_result.result:
        coin_request = CoinRequest.objects.get(celery_id=task_id)
        CoinResponse.create(
            coin_request=coin_request,
            denomination=int(celery_result.result["denomination"].split("_")[0]),
            year=0,  # celery_result.result["year"],
            celery_id=task_id,
        )
    result = {
        "task_id": task_id,
        "task_status": celery_result.status,
        "result": celery_result.result,
    }
    return JsonResponse(result, status=200)
