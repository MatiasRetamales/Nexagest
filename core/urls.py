from . import views
from django.urls import path

urlpatterns = [
    path('despacho/', views.despacho_usuario, name='despacho'),
]