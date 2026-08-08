from rest_framework import serializers
from users.models.choices import IdentificationType, Roles

class SignUpSerializer(serializers.Serializer):
    identification = serializers.CharField(max_length=20)
    identification_type = serializers.ChoiceField(choices=IdentificationType.choices)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(allow_blank=False)

class LogInSerializer(serializers.Serializer):
    identification = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, min_length=8)

class UpdateUserSerializer(serializers.Serializer):
    identification = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=False)
    identification_type = serializers.ChoiceField(choices=IdentificationType.choices, required=False)
    phone = serializers.CharField(max_length=11, required=False)
    role = serializers.ChoiceField(choices=Roles.choices, required=False)

class ResetPasswordSerializer(serializers.Serializer):
    identification = serializers.CharField(max_length=20)
    new_password = serializers.CharField(write_only=True, min_length=8)

class UserResponseSerializer(serializers.Serializer):
    identification = serializers.CharField()
    identification_type = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, allow_null=True)
    role = serializers.CharField()
    is_active = serializers.BooleanField()