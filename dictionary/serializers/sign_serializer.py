from rest_framework import serializers
from dictionary.models.choices import Categories
from dictionary.models.sign import Sign


class SignSerializer(serializers.ModelSerializer):
    sign_name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    sign_category = serializers.ChoiceField(choices=Categories.choices)

    class Meta:
        model = Sign
        fields = [
            "id",
            "created_by",
            "sign_name",
            "description",
            "sign_category",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "is_active", "created_at", "updated_at"]