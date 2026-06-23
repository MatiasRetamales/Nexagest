from django.urls import path
from .views import liberar_pedido, lista_mesas, mesa_detalle

urlpatterns = [
    path("", lista_mesas, name="lista_mesas"),
    path("<int:id>/", mesa_detalle, name="detalle_mesa"), # el <int:id> es para capturar el id de la mesa que queremos ver detalle
    path("<int:mesa_id>/liberar_pedido/", liberar_pedido, name="liberar_pedido"),  # Nueva ruta para liberar pedido 
]