from django.urls import path
from .views import add_to_excel

urlpatterns = [
    path('add_to_excel/', add_to_excel)
]
