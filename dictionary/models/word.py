import uuid
from django.db import models
from .choices import GrammaticalCategories, LanguageRegister, Status

# Create your models here.
class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='word_by')
    word_name = models.CharField(max_length=50)
    grammatical_category = models.CharField(max_length=50, choices=GrammaticalCategories.choices, default=GrammaticalCategories.VERB, null=True)
    use_level = models.CharField(max_length=30, choices=LanguageRegister.choices, default=LanguageRegister.NEUTRAL, null=True)
    description = models.TextField(null=True)
    is_active = models.CharField(max_length=50, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "words"