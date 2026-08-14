from rest_framework import serializers
from dictionary.models.choices import Categories

class SignSerializer(serializers.Serializer):
    sign_name = serializers.CharField(max_length=50)
    description = serializers.CharField()
    sign_category = serializers.ChoiceField(choices=Categories.choices)