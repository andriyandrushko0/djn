from celery import shared_task
from .apps import ModelAppConfig
from .models import CoinRequest


@shared_task
def recognize(request_id):
    result = ModelAppConfig.make_image_prediction(
        image_path=CoinRequest.objects.get(id=request_id).image.path
    )
    return {"denomination": result}
