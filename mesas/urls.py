from django.urls import path
from .views import lista_mesas, mesa_detalle

urlpatterns = [
    path("", lista_mesas, name="lista_mesas"),
    path("<int:id>/", mesa_detalle, name="detalle_mesa"), # el <int:id> es para capturar el id de la mesa que queremos ver detalle 
]