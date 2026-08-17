from django.shortcuts import render, redirect
from .models import Mesa
from pedidos.models import Pedido, PedidoItem
from django.http import HttpResponse
from django.shortcuts import get_object_or_404  # busca o lanza 404
from core.models import Restaurante
from usuarios.decoradores import tiene_acceso
from administracion.models import Caja

@tiene_acceso(['garzon', 'encargado', 'operador'])
def lista_mesas(request):
    restaurante = request.user.perfil.restaurante
    mesas = Mesa.objects.filter(restaurante=restaurante)
    caja = Caja.objects.filter(
        restaurante=restaurante,
        esta_abierta=True
    ).first()

    # Pedidos presenciales activos de cada mesa
    for mesa in mesas:
        mesa.pedido_activo = Pedido.objects.filter(
            mesa=mesa,
            origen='presencial',
            estado__in=['pendiente', 'en_preparacion', 'listo']
        ).first()

    # Pedidos realizados desde la carta online
    pedidos_online = Pedido.objects.filter(
    restaurante=restaurante,
    origen='online',
    estado__in=['pendiente', 'aceptado', 'en_preparacion', 'listo']
   ).order_by('-fecha')

    return render(request, "mesas/lista_mesas.html", {
        "mesas": mesas,
        "restaurante": restaurante,
        "caja": caja,
        "pedidos_online": pedidos_online,
    })





@tiene_acceso(['garzon', 'encargado', 'operador'])
def mesa_detalle(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    restaurante = mesa.restaurante
    
    # MODIFICACIÓN CLAVE: Buscamos pedidos que estén en 'pendiente' O 'en_preparacion'
    # Así el detalle no desaparece cuando lo mandas a cocina
    pedido_actual = Pedido.objects.filter(
        mesa=mesa, 
        estado__in=['pendiente', 'en_preparacion', 'listo'],  # Consideramos estos estados como "activos"
    ).first()

    items = []
    total = 0

    if pedido_actual:
        # Si el pedido existe, aseguramos que la mesa esté como ocupada
        if mesa.estado != "ocupada":
            mesa.estado = "ocupada"
            mesa.save()
            
        items = PedidoItem.objects.filter(pedido=pedido_actual)
        for item in items:
            total += item.subtotal()

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        mesa.estado = nuevo_estado
        mesa.save()
        return redirect('lista_mesas')

    return render(request, "mesas/detalle_mesa.html", {
        "mesa": mesa,
        "items": items,
        "total": total,
        "pedido_actual": pedido_actual,
        "restaurante": restaurante,
    })





@tiene_acceso(['garzon', 'encargado', 'operador'])
def liberar_pedido(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)

    pedido = Pedido.objects.filter(
        mesa=mesa,
        esta_pagado=True
    ).order_by("-id").first()

    if pedido:
        pedido.estado = "entregado"
        pedido.save()

        mesa.estado = "libre"
        mesa.save()

    return redirect("lista_mesas")
