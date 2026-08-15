from django.urls import path
from representations.api.representation_view import RepresentationView

urlpatterns = [
    path("get_all_representations", RepresentationView.search_all, name="get_all_representations"),
    path("get_representation", RepresentationView.get, name="get_representation"),
    path("create_representation", RepresentationView.create, name="create_representation"),
]