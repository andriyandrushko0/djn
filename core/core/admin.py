from django.contrib import admin
from .models import CoinRequest, CoinResponse

admin.site.register(CoinRequest)
admin.site.register(CoinResponse)
