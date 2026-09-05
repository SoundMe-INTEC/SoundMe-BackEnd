from django.urls import path
from dictionary.api.word_view import WordView
from dictionary.api.sign_view import SignView

urlpatterns = [
    path("get_word", WordView.get, name="get_word"),
    path("get_all_words", WordView.get_all, name="get_all_words"),
    path("create_word", WordView.create, name="create_word"),
    path("admin/words", WordView.list_admin, name="admin_list_words"),
    path("admin/words/<uuid:word_id>", WordView.update, name="admin_update_word"),
    path("admin/words/<uuid:word_id>/deactivate", WordView.deactivate, name="admin_deactivate_word"),
    path("admin/words/<uuid:word_id>/activate", WordView.activate, name="admin_activate_word"),

    path("get_all_signs", SignView.get_all, name="get_all_signs"),
    path("get_sign", SignView.get, name="get_all_signs"),
    path("create_sign", SignView.create, name="get_all_signs"),
    path("admin/signs", SignView.list_admin, name="admin_list_signs"),
    path("admin/signs/<uuid:sign_id>", SignView.update, name="admin_update_sign"),
    path("admin/signs/<uuid:sign_id>/deactivate", SignView.deactivate, name="admin_deactivate_sign"),
    path("admin/signs/<uuid:sign_id>/activate", SignView.activate, name="admin_activate_sign"),
]