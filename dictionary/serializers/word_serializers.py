from rest_framework import serializers
from dictionary.models.choices_dic import GrammaticalCategories

class WordSerializers(serializers.Serializer):
    word_name = serializers.CharField(max_length=50)
    grammatical_category = serializers.CharField(max_length=50, choices=GrammaticalCategories.choices, default=GrammaticalCategories.VERB)
    description = serializers.CharField()  