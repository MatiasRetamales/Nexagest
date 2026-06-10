from django.urls import path
from .views import (
    gestionar_pedido, cerrar_pedido, cancelar_pedido,
    eliminar_items, eliminar_item_especifico,
    marcar_pedido_listo, cocina, enviar_cocina
)

urlpatterns = [
    path("<int:id>/gestionar/", gestionar_pedido, name="gestionar_pedido"),
    path("<int:id>/cerrar/", cerrar_pedido, name="cerrar_pedido"),
    path("<int:id>/cancelar/", cancelar_pedido, name="cancelar_pedido"),
    path("<int:id>/eliminar/", eliminar_items, name="eliminar_items_a_pedido"),
    path("<int:id>/eliminar_item/", eliminar_item_especifico, name="eliminar_item_especifico"),
    path('listo/<int:pedido_id>/', marcar_pedido_listo, name='marcar_pedido_listo'),
    path('enviar-a-cocina/<int:pedido_id>/', enviar_cocina, name='enviar_cocina'),
]