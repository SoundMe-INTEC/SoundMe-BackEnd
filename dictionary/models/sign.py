import uuid
from django.db import models
from .choices import Categories, Status

# Create your models here.
class Sign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='sign_by')
    sign_name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    sign_category = models.CharField(max_length=50, choices=Categories.choices, default=Categories.SIGN, null=True)
    is_active = models.CharField(max_length=50, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class meta: 
        db_table = "signs"