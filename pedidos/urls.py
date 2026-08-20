from django.urls import path
from .views import (
    cancelar_pedido_online, gestionar_pedido, cerrar_pedido, cancelar_pedido,
    eliminar_items, eliminar_item_especifico,
    marcar_pedido_listo, cocina, enviar_cocina,
    detalle_pedido_online, aceptar_pedido_online,
    crear_pedido_online, marcar_pedido_entregado, cobrar_pedido_online, marcar_pedido_pagado, seguimiento_pedido
)

urlpatterns = [
    path("<int:id>/gestionar/", gestionar_pedido, name="gestionar_pedido"),
    path("<int:id>/cerrar/", cerrar_pedido, name="cerrar_pedido"),
    path("<int:id>/cancelar/", cancelar_pedido, name="cancelar_pedido"),
    path("<int:id>/eliminar/", eliminar_items, name="eliminar_items_a_pedido"),
    path("<int:id>/eliminar_item/", eliminar_item_especifico, name="eliminar_item_especifico"),
    path('listo/<int:pedido_id>/', marcar_pedido_listo, name='marcar_pedido_listo'),
    path('enviar-a-cocina/<int:pedido_id>/', enviar_cocina, name='enviar_cocina'),
    path('online/<int:id>/',detalle_pedido_online,name='detalle_pedido_online'),
    path('online/<int:id>/aceptar/',aceptar_pedido_online,name='aceptar_pedido_online'),
    path('online/crear/<int:restaurante_id>/',crear_pedido_online,name='crear_pedido_online'),
    path('online/<int:id>/entregar/',marcar_pedido_entregado,name='marcar_pedido_entregado'),
    path('online/<int:id>/cobrar/',cobrar_pedido_online,name='cobrar_pedido_online'),
    path('pedidos-online/<int:id>/marcar-pagado/',marcar_pedido_pagado,name='marcar_pedido_pagado'),
    path('seguimiento/<uuid:token>/',seguimiento_pedido,name='seguimiento_pedido'),
    path("pedidos-online/<int:pedido_id>/cancelar/",cancelar_pedido_online,name="cancelar_pedido_online"),
]