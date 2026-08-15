from rest_framework import serializers
from dictionary.models.choices import GrammaticalCategories, LanguageRegister
from dictionary.models.word import Word


class WordSerializer(serializers.ModelSerializer):
    word_name = serializers.CharField(max_length=50)
    grammatical_category = serializers.ChoiceField(choices=GrammaticalCategories.choices)
    use_level = serializers.ChoiceField(choices=LanguageRegister.choices, required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Word
        fields = [
            "id",
            "created_by",
            "word_name",
            "grammatical_category",
            "use_level",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "is_active", "created_at", "updated_at"]