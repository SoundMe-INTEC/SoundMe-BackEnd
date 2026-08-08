from rest_framework import serializers
from dictionary.models.choices_dic import Categories

class SignSerializer(serializers.Serializer):
    sign_name = serializers.CharField(max_length=50)
    description = serializers.CharField()
    sign_category = serializers.CharField(max_length=50, choices=Categories.choices, default=Categories.SIGN)