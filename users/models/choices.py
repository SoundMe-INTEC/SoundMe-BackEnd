from django.db.models import TextChoices

class IdentificationType (TextChoices):
    IDCARD = 'IDCard', 'idCard'
    PASSPORT = 'PASSPORT', 'passport'

class Roles (TextChoices):
    ADMIN = 'Admin', 'admin'

