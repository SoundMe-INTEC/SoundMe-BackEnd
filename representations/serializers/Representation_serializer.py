from rest_framework import serializers
from representations.models.choices import Extensions

class RepresentationSerializer(serializers.Serializer):
    url = serializers.CharField(null=False)
    extension = serializers.CharField(null=False, required=True)
    