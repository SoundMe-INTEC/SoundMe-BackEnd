from rest_framework import serializers
from users.models.choices import IdentificationType

class CreateUserSerializer (serializers.Serializer):
    identification = serializers.CharField(max_length=20)
    identification_type = serializers.ChoiceField(choices=IdentificationType.choices)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(allow_blank=True)