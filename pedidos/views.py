from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse

from carta.models import Categoria
from .models import Mesa, Producto, Pedido, PedidoItem
from core.models import Restaurante
from administracion.models import Caja
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from usuarios.decoradores import tiene_acceso
from django.utils import timezone # Importante usar este


@tiene_acceso(['garzon', 'encargado', 'operador'])
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

@tiene_acceso(['garzon', 'encargado', 'operador'])
def cerrar_pedido(request, id):
    restaurante = request.user.perfil.restaurante

    mesa = get_object_or_404(
        Mesa,
        id=id,
        restaurante=restaurante
    )

    # Buscamos el pedido activo de la mesa
    pedido_actual = Pedido.objects.filter(
        mesa=mesa,
        estado__in=["pendiente", "en_preparacion", "listo"],
        restaurante=restaurante,
        esta_pagado=False
    ).first()

    # Si no hay pedido
    if not pedido_actual:
        return render(request, "pedidos/cerrar_pedido.html", {
            "mesa": mesa,
            "pedido_actual": None,
            "items": [],
            "total": 0,
            "propina": 0,
            "total_con_propina": 0
        })

    # Productos del pedido
    items = PedidoItem.objects.filter(
        pedido=pedido_actual
    )

    # Total
    total = sum(
        item.subtotal()
        for item in items
    )

    # Propina
    propina = 0

    if pedido_actual.restaurante.propina_activa:
        propina = (
            total *
            (
                pedido_actual.restaurante.porcentaje_propina / 100
            )
        )

    total_con_propina = total + propina

    # =========================
    # PROCESAR PAGO
    # =========================

    if request.method == "POST":

        # Método de pago seleccionado
        metodo_pago = request.POST.get("metodo_pago")

        # Verificamos que exista
        if metodo_pago not in [
            "efectivo",
            "tarjeta",
            "transferencia"
        ]:
            messages.error(
                request,
                "Debes seleccionar un método de pago."
            )

            return redirect(
                "cerrar_pedido",
                id=mesa.id
            )

        # Propina
        usar_propina = (
            request.POST.get("usar_propina") == "1"
        )

        if (
            pedido_actual.restaurante.propina_activa
            and usar_propina
        ):

            pedido_actual.propina_aplicada = True
            pedido_actual.monto_propina = propina

            total_final = total_con_propina

        else:

            pedido_actual.propina_aplicada = False
            pedido_actual.monto_propina = 0

            total_final = total

        # =========================
        # CAJA
        # =========================

        caja_activa = Caja.objects.filter(
            restaurante=restaurante,
            esta_abierta=True
        ).first()

        if caja_activa:
            pedido_actual.sesion_caja = caja_activa

        # =========================
        # GUARDAR PAGO
        # =========================

        pedido_actual.metodo_pago = metodo_pago

        pedido_actual.esta_pagado = True

        pedido_actual.total = total_final

        pedido_actual.fecha_pago = timezone.now()

        pedido_actual.save()

        # =========================
        # ACTUALIZAR MESA
        # =========================

        mesa.estado = "ocupada"
        mesa.save()

        messages.success(
            request,
            f"Pago registrado correctamente. "
            f"Método: {pedido_actual.get_metodo_pago_display()}"
        )

        return redirect("lista_mesas")

    # =========================
    # MOSTRAR PANTALLA
    # =========================

    return render(
        request,
        "pedidos/cerrar_pedido.html",
        {
            "mesa": mesa,
            "pedido_actual": pedido_actual,
            "items": items,
            "total": total,
            "propina": propina,
            "total_con_propina": total_con_propina
        }
    )

@tiene_acceso(['encargado'])
def cancelar_pedido(request, id):
    restaurante = request.user.perfil.restaurante

    mesa = get_object_or_404(Mesa, id=id, restaurante=restaurante)

    # MODIFICACIÓN: Buscamos pedidos que estén en 'pendiente' O 'en_preparacion'
    # Así permitimos cancelar algo que ya se mandó a cocina por error
    pedido_actual = Pedido.objects.filter(
        mesa=mesa,
        estado__in=["pendiente", "en_preparacion", "listo"],
        esta_pagado=False,
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


@tiene_acceso(['garzon', 'encargado', 'operador'])
def eliminar_items(request, id):
    restaurante = request.user.perfil.restaurante

    mesa = get_object_or_404(Mesa, id=id, restaurante=restaurante)

    pedido_actual = Pedido.objects.filter(
        mesa=mesa,
        estado__in=["pendiente", "en_preparacion", "listo"],  # Consideramos estos estados como "activos"
        restaurante=restaurante,
        esta_pagado=False,
    ).first()

    items = []

    if pedido_actual:
        items = PedidoItem.objects.filter(pedido=pedido_actual)

    return render(request, "pedidos/eliminar_items_a_pedido.html", {
        "mesa": mesa,
        "pedido_actual": pedido_actual,
        "items": items
    })



@tiene_acceso(['garzon', 'encargado', 'operador'])
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
  
    
@tiene_acceso(['cocinero', 'administrador', 'encargado', 'operador'])
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
        "restaurante": restaurante, 
    })

@tiene_acceso(['garzon', 'encargado', 'operador'])
def enviar_cocina(request, pedido_id):
    restaurante = request.user.perfil.restaurante
    pedido = get_object_or_404(Pedido, id=pedido_id, restaurante=restaurante)

    if pedido.estado in ["pendiente", "listo", "en_preparacion", "aceptado"]:
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

    if pedido.origen == 'online':
     return redirect('detalle_pedido_online', id=pedido.id)
    else:
     return redirect('detalle_mesa', id=pedido.mesa.id)


@tiene_acceso(['cocinero', 'encargado', 'operador'])
def marcar_pedido_listo(request, pedido_id):
    restaurante = request.user.perfil.restaurante
    pedido = get_object_or_404(Pedido, id=pedido_id, restaurante=restaurante)
    pedido.estado = 'listo'
    pedido.save()
    return redirect('cocina')


@tiene_acceso(['garzon', 'encargado', 'operador'])
def detalle_pedido_online(request, id):
    restaurante = request.user.perfil.restaurante

    pedido = get_object_or_404(
        Pedido,
        id=id,
        restaurante=restaurante,
        origen='online'
    )

    items = pedido.items.all()

    total = sum(item.subtotal() for item in items)

    return render(request, "pedidos/detalle_pedido_online.html", {
        "pedido": pedido,
        "items": items,
        "total": total,
        "restaurante": restaurante,
    })


@tiene_acceso(['garzon', 'encargado', 'operador'])
def aceptar_pedido_online(request, id):

    restaurante = request.user.perfil.restaurante

    pedido = get_object_or_404(
        Pedido,
        id=id,
        restaurante=restaurante,
        origen='online'
    )

    if request.method == "POST":

        if pedido.estado == 'pendiente':

            # Transferencia debe estar pagada antes de enviar a cocina
            if pedido.metodo_pago == 'transferencia' and not pedido.esta_pagado:

                messages.error(
                    request,
                    'Debes verificar el pago por transferencia antes de aceptar el pedido.'
                )

                return redirect(
                    'detalle_pedido_online',
                    id=pedido.id
                )

            pedido.estado = 'en_preparacion'
            pedido.enviado_a_cocina = timezone.now()
            pedido.total_envios += 1

            pedido.save()

            pedido.items.filter(
                enviado_a_cocina=False
            ).update(
                enviado_a_cocina=True,
                numero_envio=pedido.total_envios
            )

            messages.success(
                request,
                f"Pedido online #{pedido.id} enviado a cocina."
            )

    return redirect(
        'detalle_pedido_online',
        id=pedido.id
    )

@require_POST
def crear_pedido_online(request, restaurante_id):

    restaurante = get_object_or_404(
        Restaurante,
        id=restaurante_id
    )

    # ========================================
    # VERIFICAR PEDIDOS ONLINE
    # ========================================

    if not restaurante.pedidos_online_activos:

        return JsonResponse({
            'error': 'Los pedidos online no están disponibles en este momento.'
        }, status=400)


    # ========================================
    # DATOS DEL CLIENTE
    # ========================================

    nombre_cliente = request.POST.get(
        'nombre_cliente',
        ''
    ).strip()

    telefono_cliente = request.POST.get(
        'telefono_cliente',
        ''
    ).strip()


    # ========================================
    # TIPO DE ENTREGA
    # ========================================

    tipo_entrega = request.POST.get(
        'tipo_entrega',
        ''
    )


    if tipo_entrega not in ['retiro', 'delivery']:

        return JsonResponse({
            'error': 'Tipo de entrega no válido.'
        }, status=400)


    # ========================================
    # VALIDAR RETIRO / DELIVERY
    # ========================================

    if (
        tipo_entrega == 'retiro'
        and not restaurante.acepta_retiro
    ):

        return JsonResponse({
            'error': 'Este local no permite retiro en este momento.'
        }, status=400)


    if (
        tipo_entrega == 'delivery'
        and not restaurante.acepta_delivery
    ):

        return JsonResponse({
            'error': 'Este local no tiene delivery disponible.'
        }, status=400)


    # ========================================
    # DIRECCIÓN
    # ========================================

    direccion_entrega = request.POST.get(
        'direccion_entrega',
        ''
    ).strip()


    if (
        tipo_entrega == 'delivery'
        and not direccion_entrega
    ):

        return JsonResponse({
            'error': 'Debes ingresar una dirección de entrega.'
        }, status=400)


    # ========================================
    # MÉTODO DE PAGO
    # ========================================

    metodo_pago = request.POST.get(
        'metodo_pago',
        ''
    )


    if not metodo_pago:

        return JsonResponse({
            'error': 'Debes seleccionar un método de pago.'
        }, status=400)


    # ========================================
    # VALIDAR MÉTODO DE PAGO
    # ========================================

    if (
        metodo_pago == 'efectivo'
        and not restaurante.acepta_pago_local
    ):

        return JsonResponse({
            'error': 'El pago en local no está disponible.'
        }, status=400)


    if (
        metodo_pago == 'transferencia'
        and not restaurante.acepta_pago_transferencia
    ):

        return JsonResponse({
            'error': 'La transferencia bancaria no está disponible.'
        }, status=400)


    if metodo_pago not in [
        'efectivo',
        'transferencia'
    ]:

        return JsonResponse({
            'error': 'Método de pago no válido.'
        }, status=400)


    # ========================================
    # PRODUCTOS
    # ========================================

    productos_json = request.POST.get(
        'productos',
        '[]'
    )


    import json


    try:

        productos = json.loads(
            productos_json
        )

    except json.JSONDecodeError:

        return JsonResponse({
            'error': 'El pedido no es válido.'
        }, status=400)


    if not productos:

        return JsonResponse({
            'error': 'El carrito está vacío.'
        }, status=400)


    # ========================================
    # CREAR PEDIDO
    # ========================================

    pedido = Pedido.objects.create(

        restaurante=restaurante,

        origen='online',

        estado='pendiente',

        nombre_cliente=nombre_cliente,

        telefono_cliente=telefono_cliente,

        tipo_entrega=tipo_entrega,

        direccion_entrega=(
            direccion_entrega
            if tipo_entrega == 'delivery'
            else ''
        ),

        metodo_pago=metodo_pago,

        estado_pago='pendiente',

        esta_pagado=False

    )


    # ========================================
    # CREAR PRODUCTOS DEL PEDIDO
    # ========================================

    total = 0


    for producto_data in productos:

        producto = get_object_or_404(

            Producto,

            id=producto_data['id'],

            restaurante=restaurante,

            disponibilidad='disponible'

        )


        cantidad = int(
            producto_data['cantidad']
        )


        if cantidad <= 0:
            continue


        PedidoItem.objects.create(

            pedido=pedido,

            producto=producto,

            cantidad=cantidad,

            precio_unitario=producto.precio

        )


        total += (
            producto.precio *
            cantidad
        )


    # ========================================
    # GUARDAR TOTAL
    # ========================================

    pedido.total = total

    pedido.save()


    # ========================================
    # RESPUESTA
    # ========================================

    seguimiento_url = request.build_absolute_uri(
    reverse(
        'seguimiento_pedido',
        args=[pedido.token_seguimiento]
    )
)

    return JsonResponse({

    'success': True,

    'pedido_id': pedido.id,

    'seguimiento_url': request.build_absolute_uri(
        reverse(
            'seguimiento_pedido',
            args=[pedido.token_seguimiento]
        )
    )

})


@tiene_acceso(['garzon', 'encargado', 'operador'])
def marcar_pedido_entregado(request, id):

    restaurante = request.user.perfil.restaurante

    pedido = get_object_or_404(
        Pedido,
        id=id,
        restaurante=restaurante,
        origen='online'
    )

    if request.method == "POST":

        # ========================================
        # DELIVERY
        # ========================================

        if pedido.tipo_entrega == 'delivery':

            # LISTO → EN CAMINO
            if pedido.estado == 'listo':

                pedido.estado = 'en_camino'

                messages.success(
                    request,
                    f"Pedido online #{pedido.id} va en camino."
                )

            # EN CAMINO → ENTREGADO
            elif pedido.estado == 'en_camino':

                pedido.estado = 'entregado'

                messages.success(
                    request,
                    f"Pedido online #{pedido.id} fue entregado."
                )

        # ========================================
        # RETIRO
        # ========================================

        else:

            if pedido.estado == 'listo':

                pedido.estado = 'entregado'

                messages.success(
                    request,
                    f"Pedido online #{pedido.id} marcado como entregado."
                )

        pedido.save()

    return redirect(
        'detalle_pedido_online',
        id=pedido.id
    )


@tiene_acceso(['garzon', 'encargado', 'operador'])
def cobrar_pedido_online(request, id):

    restaurante = request.user.perfil.restaurante

    pedido = get_object_or_404(
        Pedido,
        id=id,
        restaurante=restaurante,
        origen='online',
        estado='listo',
        esta_pagado=False
    )

    items = pedido.items.all()

    total = sum(
        item.subtotal()
        for item in items
    )

    propina = 0

    if restaurante.propina_activa:
        propina = (
            total *
            restaurante.porcentaje_propina / 100
        )

    total_con_propina = total + propina

    if request.method == "POST":

        metodo_pago = request.POST.get("metodo_pago")

        if metodo_pago not in [
            "efectivo",
            "tarjeta",
            "transferencia"
        ]:
            messages.error(
                request,
                "Debes seleccionar un método de pago."
            )

            return redirect(
                "cobrar_pedido_online",
                id=pedido.id
            )

        usar_propina = (
            request.POST.get("usar_propina") == "1"
        )

        if restaurante.propina_activa and usar_propina:

            pedido.propina_aplicada = True
            pedido.monto_propina = propina
            total_final = total_con_propina

        else:

            pedido.propina_aplicada = False
            pedido.monto_propina = 0
            total_final = total

        # Buscar caja abierta
        caja_activa = Caja.objects.filter(
            restaurante=restaurante,
            esta_abierta=True
        ).first()

        if caja_activa:
            pedido.sesion_caja = caja_activa

        # Registrar pago
        pedido.metodo_pago = metodo_pago
        pedido.esta_pagado = True
        pedido.total = total_final
        pedido.fecha_pago = timezone.now()

        pedido.save()

        messages.success(
            request,
            f"Pago registrado correctamente. "
            f"Método: {pedido.get_metodo_pago_display()}"
        )

        return redirect(
            "detalle_pedido_online",
            id=pedido.id
        )

    return render(
        request,
        "pedidos/cobrar_pedido_online.html",
        {
            "pedido": pedido,
            "items": items,
            "total": total,
            "propina": propina,
            "total_con_propina": total_con_propina,
        }
    )
    
    
    
@tiene_acceso(['garzon', 'encargado', 'operador'])
def marcar_pedido_pagado(request, id):

    restaurante = request.user.perfil.restaurante

    pedido = get_object_or_404(
        Pedido,
        id=id,
        restaurante=restaurante,
        origen='online'
    )

    if request.method == "POST":

        # ========================================
        # VERIFICAR QUE EXISTA UNA CAJA ABIERTA
        # ========================================

        caja_abierta = Caja.objects.filter(
            restaurante=restaurante,
            esta_abierta=True
        ).first()

        if not caja_abierta:

            messages.error(
                request,
                'No hay una caja abierta. Debes abrir la caja antes de registrar el pago.'
            )

            return redirect(
                'detalle_pedido_online',
                id=pedido.id
            )

        # ========================================
        # MARCAR PEDIDO COMO PAGADO
        # ========================================

        pedido.esta_pagado = True
        pedido.estado_pago = 'confirmado'
        pedido.fecha_pago = timezone.now()

        # ========================================
        # ASOCIAR PEDIDO A LA CAJA ACTUAL
        # ========================================

        pedido.sesion_caja = caja_abierta

        pedido.save()

        messages.success(
            request,
            f"Pago del pedido online #{pedido.id} verificado correctamente."
        )

    return redirect(
        'detalle_pedido_online',
        id=pedido.id
    )
    
    
    
def seguimiento_pedido(request, token):

    pedido = get_object_or_404(
        Pedido,
        token_seguimiento=token,
        origen='online'
    )

    # ========================================
    # SI ES UNA CONSULTA AJAX
    # ========================================

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse({
           'estado': pedido.estado,
           'estado_display': pedido.get_estado_display(),
           'esta_pagado': pedido.esta_pagado,
           'tipo_entrega': pedido.tipo_entrega,
        })


    # ========================================
    # PEDIDO FINALIZADO
    # ========================================

    if pedido.estado in [
        'entregado',
        'cancelado'
    ]:

        return render(
            request,
            'pedidos/seguimiento_expirado.html',
            {
                'pedido': pedido,
            }
        )


    # ========================================
    # PRODUCTOS
    # ========================================

    items = pedido.items.all()

    total = sum(
        item.subtotal()
        for item in items
    )


    return render(
        request,
        'pedidos/seguimiento_pedido.html',
        {
            'pedido': pedido,
            'items': items,
            'total': total,
        }
    )