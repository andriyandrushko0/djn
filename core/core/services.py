import os
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import APIException
from .exceptions import ImageRequired, FileNotAllowed, CoinImageException


def renamer_image(instance, filename):
    from uuid import uuid4
    from datetime import datetime

    upload_to = "media"
    ext = filename.split(".")[-1]
    if instance.pk:
        filename = "{}-{}.{}".format(instance.pk, datetime.now(), ext)
    else:
        filename = "{}.{}".format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


def validate_request_file(request_params: dict, media=False):
    if not request_params.get("file"):
        raise APIException("Bad file")

    return request_params.get("file")


def validate_request(request):
    data = request.FILES.get("image")
    if data and type(data) is not str:
        if data.name.split(".")[-1].lower() not in ["png", "jpg", "jpeg"]:
            raise FileNotAllowed(data)
        else:
            return data
    else:
        raise ImageRequired()


def crop_image(image):
    from io import BytesIO

    pillow_image = Image.open(image)
    pillow_image = pillow_image.convert("RGB")
    width, height = pillow_image.size
    is_portrait = True if height > width else False
    temp = BytesIO()

    if is_portrait:
        coeff = int((height - width) / 2)
        cropped = pillow_image.crop((0, coeff, width, coeff + width))
    elif width == height:
        return image
    else:
        coeff = int((width - height) / 2)
        cropped = pillow_image.crop((coeff, 0, coeff + height, height))

    cropped.save(fp=temp, format="JPEG")
    return InMemoryUploadedFile(
        temp, None, "temp.jpg", "image/jpeg", temp.getbuffer().nbytes, None
    )


def get_image(request):
    return crop_image(validate_request(request))
