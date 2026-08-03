from django.db import models

class Categories(models.TextChoices):
    WORD = 'word', 'Word'
    SIGN = 'sign', 'Sign'
    REPRESENTATION = 'representation', 'Representation'
    
class Status(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'