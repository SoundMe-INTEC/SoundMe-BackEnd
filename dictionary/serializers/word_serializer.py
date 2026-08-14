from rest_framework import serializers
from dictionary.models.choices import GrammaticalCategories

class WordSerializer(serializers.Serializer):
    word_name = serializers.CharField(max_length=50)
    grammatical_category = serializers.ChoiceField(choices=GrammaticalCategories.choices)
    description = serializers.CharField()  