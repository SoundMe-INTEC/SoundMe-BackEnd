from django.urls import path
from . import user_api

urlpatterns = [
    path('', user_api.test)  
]