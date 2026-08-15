from django.db import models


class Extensions(models.TextChoices):
    IMG = "img", "img"
    PNG = "png", "png"