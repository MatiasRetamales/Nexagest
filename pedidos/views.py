from django.shortcuts import render, get_object_or_404, redirect

from carta.models import Categoria
from .models import Mesa, Producto, Pedido, PedidoItem
from core.models import Restaurante
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from usuarios.decoradores import solo_cocinero, solo_admin_restaurante
from django.utils import timezone # Importante usar este


def gestionar_pedido(request, id):
    restaurante = request.user.perfil.restaurante
    mesa = get_object_or_404(Mesa, id=id, restaurante=restaurante)
    categorias = Categoria.objects.filter(restaurante=restaurante)
    productos = Producto.objects.filter(restaurante=restaurante)
    
    pedido_actual = Pedido.objects.filter(
        mesa=mesa,
        estado__in=['pendiente', 'en_preparacion', 'listo'],
        restaurante=restaurante
    ).first()

    if request.method == "POST":
        # 1. Capturamos el nombre siempre
        nombre_cliente = request.POST.get("nombre_cliente", "").strip()
        
        # 2. Recopilamos los productos
        productos_a_agregar = []
        for prod in productos:
            cantidad_str = request.POST.get(f"cantidad_{prod.id}", "0")
            cantidad = int(cantidad_str)
            if cantidad > 0:
                observacion = request.POST.get(f"obs_{prod.id}", "").strip()
                productos_a_agregar.append({
                    'producto': prod,
                    'cantidad': cantidad,
                    'observacion': observacion
                })

        # 3. Procesamos pedido solo si hay productos
        if productos_a_agregar:
            # Si NO existe, lo creamos
            if not pedido_actual:
                pedido_actual = Pedido.objects.create(
                    mesa=mesa,
                    estado='pendiente',
                    garzon=request.user if request.user.is_authenticated else None,
                    restaurante=restaurante,
                    nombre_cliente=nombre_cliente if restaurante.tipo_local == 'local' else None
                )
            # Si YA existía, actualizamos el nombre
            elif restaurante.tipo_local == 'local':
                pedido_actual.nombre_cliente = nombre_cliente
                pedido_actual.save()

            # 4. Guardamos los items
            for item in productos_a_agregar:
                PedidoItem.objects.create(
                    pedido=pedido_actual,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['producto'].precio,
                    observacion=item['observacion']
                )
        
        # El redirect es obligatorio aquí
        return redirect('gestionar_pedido', id=mesa.id)

    # ESTE ES EL RETURN QUE FALTABA
    # Se ejecuta cuando es un GET o cuando el POST no agregó nada
    return render(request, "pedidos/gestionar_pedido.html", {
        "mesa": mesa,
        "productos": productos,
        "categorias": categorias,
        "restaurante": restaurante,
        "pedido_actual": pedido_actual,
    })

def cerrar_pedido(request, id):
    restaurante = request.user.perfil.restaurante

    mesa = get_object_or_404(Mesa, id=id, restaurante=restaurante)

    # MODIFICACIÓN: Buscamos el pedido en cualquier estado "activo"
    # Pendiente (si no pasó por cocina) o En Preparación (si ya se envió)
    pedido_actual = Pedido.objects.filter(
        mesa=mesa,
        estado__in=["pendiente", "en_preparacion", "listo"],
        restaurante=restaurante
    ).first()

    # Si no hay pedido en esos estados, devolvemos la vista vacía
    if not pedido_actual:
        return render(request, "pedidos/cerrar_pedido.html", {
            "mesa": mesa,
            "pedido_actual": None,
            "items": [],
            "total": 0
        })

    items = PedidoItem.objects.filter(pedido=pedido_actual)
    total = sum(item.subtotal() for item in items)

    if request.method == "POST":
     pedido_actual.estado = "pagado"
     pedido_actual.total = total 
     # Si no quieres crear un campo nuevo aún, 
     # asegúrate de que el dashboard use 'fecha'
     pedido_actual.fecha = timezone.now() 
     pedido_actual.fecha_pago = timezone.now()  # También actualizamos la fecha de pago
     pedido_actual.save()

        # Liberamos la mesa para el siguiente cliente de Cartagena
     mesa.estado = "libre"
     mesa.save()

     return redirect('lista_mesas') # Mejor volver a la lista para ver qué otra mesa atender

    return render(request, "pedidos/cerrar_pedido.html", {
        "mesa": mesa,
        "pedido_actual": pedido_actual,
        "items": items,
        "total": total,
    })


def cancelar_pedido(request, id):
    restaurante = request.user.perfil.restaurante

    mesa = get_object_or_404(Mesa, id=id, restaurante=restaurante)

    # MODIFICACIÓN: Buscamos pedidos que estén en 'pendiente' O 'en_preparacion'
    # Así permitimos cancelar algo que ya se mandó a cocina por error
    pedido_actual = Pedido.objects.filter(
        mesa=mesa,
        estado__in=["pendiente", "en_preparacion", "listo"],
        restaurante=restaurante
    ).first()

    items = []
    total = 0

    if pedido_actual:
        items = PedidoItem.objects.filter(pedido=pedido_actual)
        total = sum(item.subtotal() for item in items)

    if request.method == "POST":
        if pedido_actual:
            pedido_actual.estado = "cancelado"
            pedido_actual.save()

        # Liberamos la mesa siempre al cancelar
        mesa.estado = "libre"
        mesa.save()

        # Redirigimos a la lista de mesas (o al detalle)
        return redirect('lista_mesas') 

    return render(request, "pedidos/cancelar_pedido.html", {
        "mesa": mesa,
        "pedido_actual": pedido_actual,
        "items": items,
        "total": total
    })


def eliminar_items(request, id):
    restaurante = request.user.perfil.restaurante

    mesa = get_object_or_404(Mesa, id=id, restaurante=restaurante)

    pedido_actual = Pedido.objects.filter(
        mesa=mesa,
        estado__in=["pendiente", "en_preparacion", "listo"],  # Consideramos estos estados como "activos"
        restaurante=restaurante
    ).first()

    items = []

    if pedido_actual:
        items = PedidoItem.objects.filter(pedido=pedido_actual)

    return render(request, "pedidos/eliminar_items_a_pedido.html", {
        "mesa": mesa,
        "pedido_actual": pedido_actual,
        "items": items
    })



def eliminar_item_especifico(request, id):
    restaurante = request.user.perfil.restaurante

    if request.method == "POST":
        item = get_object_or_404(
            PedidoItem,
            id=id,
            pedido__restaurante=restaurante
        )

        pedido = item.pedido
        mesa = pedido.mesa # Guardamos la mesa para usarla después

        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

        
        # Después de borrar, preguntamos: ¿Quedó algún otro producto en este pedido?
        if not pedido.items.exists(): 
            pedido.delete()        # Si no hay nada, borramos el pedido
            mesa.estado = "libre"  # Y liberamos la mesa
            mesa.save()

        return redirect('detalle_mesa', id=mesa.id)
  
    
@solo_cocinero
def cocina(request):
    restaurante = request.user.perfil.restaurante
    pedidos_pendientes = Pedido.objects.filter(
        restaurante=restaurante,
        estado="en_preparacion"
    )

    for pedido in pedidos_pendientes:
        pedido.items_cocina = pedido.items.filter(numero_envio=pedido.total_envios)

    return render(request, "pedidos/cocina.html", {
        "pedidos_pendientes": pedidos_pendientes,
        "restaurante": restaurante, # <--- ¡Solo faltaba esto!
    })

def enviar_cocina(request, pedido_id):
    restaurante = request.user.perfil.restaurante
    pedido = get_object_or_404(Pedido, id=pedido_id, restaurante=restaurante)

    if pedido.estado in ["pendiente", "listo"]:
        pedido.total_envios += 1
        pedido.estado = "en_preparacion"
        pedido.enviado_a_cocina = timezone.now()
        pedido.save()

        pedido.items.filter(enviado_a_cocina=False).update(
            enviado_a_cocina=True,
            numero_envio=pedido.total_envios
        )
        messages.success(request, f"Pedido {pedido.id} enviado a cocina.")
    else:
        messages.error(request, f"Pedido {pedido.id} no se puede enviar a cocina.")

    return redirect('detalle_mesa', id=pedido.mesa.id)


def marcar_pedido_listo(request, pedido_id):
    restaurante = request.user.perfil.restaurante
    pedido = get_object_or_404(Pedido, id=pedido_id, restaurante=restaurante)
    pedido.estado = 'listo'
    pedido.save()
    return redirect('vista_cocina')
