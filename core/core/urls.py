from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.api_roots, name="api_roots"),
    path("recognize/", views.recognize_request, name="recognize"),
    path("recognize/<task_id>/", views.recognize_response, name="recognize_response"),
]
