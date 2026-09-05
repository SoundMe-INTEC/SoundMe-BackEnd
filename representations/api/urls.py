from django.urls import path
from representations.api.representation_view import RepresentationView

urlpatterns = [
    path("get_all_representations", RepresentationView.search_all, name="get_all_representations"),
    path("get_representation", RepresentationView.get, name="get_representation"),
    path("create_representation", RepresentationView.create, name="create_representation"),
    path("admin/representations", RepresentationView.list_admin, name="admin_list_representations"),
    path("admin/representations/<uuid:representation_id>", RepresentationView.update, name="admin_update_representation"),
    path("admin/representations/<uuid:representation_id>/deactivate", RepresentationView.deactivate, name="admin_deactivate_representation"),
    path("admin/representations/<uuid:representation_id>/activate", RepresentationView.activate, name="admin_activate_representation"),
]