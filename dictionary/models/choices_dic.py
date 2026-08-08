from django.db import models

class Categories(models.TextChoices):
    WORD = "word", "Word"
    SIGN = "sign", "Sign"
    REPRESENTATION = "representation", "Representation"

class Status(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

class GrammaticalCategories(models.TextChoices):
    NOUN = "noun", "Noun"
    VERB = "verb", "Verb"
    ADJECTIVE = "adjective", "Adjective"
    ADVERB = "adverb", "Adverb"
    PRONOUN = "pronoun", "Pronoun"
    PREPOSITION = "preposition", "Preposition"
    CONJUNCTION = "conjunction", "Conjunction"
    INTERJECTION = "interjection", "Interjection"
    DETERMINER = "determiner", "Determiner"
    ARTICLE = "article", "Article"
    NUMERAL = "numeral", "Numeral"
    
class UsageContext(models.TextChoices):
    EDUCATIONAL = "educational", "Educational"
    EVERYDAY = "everyday", "Everyday"
    FORMAL = "formal", "Formal"
    INFORMAL = "informal", "Informal"
    PROFESSIONAL = "professional", "Professional"
    ACADEMIC = "academic", "Academic"
    TECHNICAL = "technical", "Technical"
    LEGAL = "legal", "Legal"
    MEDICAL = "medical", "Medical"
    RELIGIOUS = "religious", "Religious"
    
class LanguageRegister(models.TextChoices):
    COLLOQUIAL = "colloquial", "Colloquial"
    INFORMAL = "informal", "Informal"
    NEUTRAL = "neutral", "Neutral"
    FORMAL = "formal", "Formal"
    TECHNICAL = "technical", "Technical"
    SCIENTIFIC = "scientific", "Scientific"
    LITERARY = "literary", "Literary"
    SLANG = "slang", "Slang"
    ARCHAIC = "archaic", "Archaic"