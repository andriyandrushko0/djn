from django.db import models
from .services import renamer_image


class CoinRequest(models.Model):
    image = models.ImageField(upload_to=renamer_image)
    date_time = models.DateTimeField(auto_now=True)
    celery_id = models.CharField(max_length=255)


class CoinResponse(models.Model):
    coin_request = models.ForeignKey(
        CoinRequest, on_delete=models.CASCADE, related_name="coin_request"
    )
    denomination = models.IntegerField()
    year = models.IntegerField()
    date_time = models.DateTimeField(auto_now=True)
    celery_id = models.CharField(max_length=255)

    @staticmethod
    def create(coin_request, denomination, year, celery_id):
        new = CoinResponse(
            coin_request=coin_request,
            denomination=denomination,
            year=year,
            celery_id=celery_id,
        )
        new.save()
