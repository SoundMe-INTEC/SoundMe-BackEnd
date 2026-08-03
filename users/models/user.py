import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from . import choices
from .manager.user_manager import UserManager

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identification = models.CharField(max_length=20, unique=True)
    username = None
    identification_type = models.CharField(max_length=20, choices=choices.IdentificationType.choices)
    role = models.CharField(max_length=20, choices=choices.Roles.choices, default=choices.Roles.ADMIN)
    phone = models.CharField(max_length=11, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "identification" 
    REQUIRED_FIELDS = ["email", "identification_type"]

    objects = UserManager() #type: ignore

    class Meta:  # type: ignore
        db_table = "users"

    def __str__(self):
        return self.identification
