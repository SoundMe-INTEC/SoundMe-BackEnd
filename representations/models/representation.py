from django.db import models
import uuid 
from representations.models.choices import Extensions

# Create your models here.

class Representation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sign_id = models.ForeignKey('dictionary.Sign', on_delete=models.CASCADE, related_name="idsigns")
    create_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="representationsby")
    extension = models.CharField(max_length=20, choices=Extensions.choices, default=Extensions.choices.WAV, null=False)
    url = models.TextField(null=False)
    is_primary = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)   
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = "sign_representation" 
