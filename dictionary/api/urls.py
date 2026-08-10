from django.urls import path
from dictionary.api.word_view import WordView
from dictionary.api.sign_view import SignView

urlpatterns = [
    path("get_word", WordView.get, name="get_word"),
    path("get_all_words", WordView.get_all, name="get_all_words"),

    path("get_all_signs", SignView.get_all, name="get_all_signs"),
    path("get_sign", SignView.get, name="get_all_signs"),
    path("create_sign", SignView.create, name="get_all_signs")
]