from django.urls import path
from .views import main

urlpatterns = [
    path('<str:filepath>/<int:examno>/',main)
]