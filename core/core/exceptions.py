import json
from rest_framework.exceptions import APIException


class ImageRequired(Exception):
    def __str__(self):
        return "Image is required"

    def to_json(self):
        return json.dumps({"error": "Image is required"})


class FileNotAllowed(Exception):
    def __init__(self, file):
        self.file_name = file.name
        self.message = f"File: {self.file_name} is not allowed file type"

    def __str__(self):
        return self.message

    def to_json(self):
        return json.dumps({"error": self.message})


class CoinImageException(BaseException):
    pass
