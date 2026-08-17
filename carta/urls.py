from django.urls import path
from . import views

urlpatterns = [
    path('<int:restaurante_id>/', views.carta_publica, name='carta_publica'),
]