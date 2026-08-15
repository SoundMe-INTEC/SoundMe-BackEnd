from rest_framework import serializers
from representations.models.choices import Extensions
from representations.models.representation import Representation


class RepresentationSerializer(serializers.ModelSerializer):
    url = serializers.CharField(required=True, allow_blank=False)
    extension = serializers.ChoiceField(choices=Extensions.choices)

    class Meta:
        model = Representation
        fields = [
            "id",
            "sign_id",
            "create_by",
            "extension",
            "url",
            "is_primary",
            "order",
            "is_active",
            "create_at",
            "update_at",
        ]
        read_only_fields = ["id", "create_at", "update_at", "create_by", "sign_id"]