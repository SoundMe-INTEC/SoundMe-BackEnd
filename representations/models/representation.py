from django.db import models
import uuid 

# Create your models here.
class Representation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sign_id = ''
    create_by = ''
    extension = ''
    url = ''
    is_primary = ''
    order = ''
    active = ''
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table: "sign_representation" 
