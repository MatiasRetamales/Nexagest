from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta # Necesitamos estas para los cálculos
from django.contrib import messages
from administracion.models import Caja
from pedidos.models import Pedido
from core.models import Restaurante
from usuarios.decoradores import tiene_acceso
from pedidos.forms import ProductoForm, CategoriaForm
from django.contrib.auth.models import User
from usuarios.models import Perfil



@tiene_acceso(['administrador'])
def dashboard(request):
    restaurante = request.user.perfil.restaurante
    
    # 1. Intentamos atrapar la fecha de la URL: /dashboard/?fecha=2026-05-20
    fecha_url = request.GET.get('fecha')
    
    # 2. Lógica de decisión
    if fecha_url:
        # Si el usuario mandó una fecha, la convertimos de "texto" a "fecha real"
        fecha_actual = datetime.strptime(fecha_url, '%Y-%m-%d').date()
    else:
        # Si no mandó nada, por defecto es hoy
        fecha_actual = timezone.now().date()
    
    # 3. El Filtro: Usamos fecha_actual (que puede ser hoy, ayer o cualquier día)
    pedidos_dia = Pedido.objects.filter(
        restaurante=restaurante,
        fecha_pago__date=fecha_actual,
        esta_pagado=True
    )
    
    total_ventas = pedidos_dia.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_pedidos = pedidos_dia.count()
    
    # 4. Calculamos "Ayer" y "Mañana" para los botones del HTML
    fecha_ayer = fecha_actual - timedelta(days=1)
    fecha_manana = fecha_actual + timedelta(days=1)
    
    context = {
        'total_ventas': total_ventas,
        'cantidad_pedidos': cantidad_pedidos,
        'fecha': fecha_actual,
        'fecha_ayer': fecha_ayer.strftime('%Y-%m-%d'),   # Lo mandamos como texto para la URL
        'fecha_manana': fecha_manana.strftime('%Y-%m-%d'),
    }
    return render(request, 'administracion/dashboard.html', context)




@tiene_acceso(['administrador', 'encargado'])
def menu_admin(request):
    # 1. Buscamos el restaurante en la base de datos
    restaurante = request.user.perfil.restaurante
    
    # 2. Lo metemos en el diccionario de contexto
    context = {
        'restaurante': restaurante
    }
    
    # 3. Lo pasamos al render
    return render(request, 'administracion/menu_admin.html', context)


@tiene_acceso(['administrador'])
def toggle_estado_local(request):
    if request.method == "POST":
        # Traemos el primer restaurante (asumiendo que solo tienes uno configurado)
        restaurante = request.user.perfil.restaurante
        
        if restaurante:
            if restaurante.estado == 'abierto':
                restaurante.estado = 'cerrado'
            else:
                restaurante.estado = 'abierto'
            
            restaurante.save()
            
    return redirect('menu_admin') # Te devuelve a la pantalla donde está el botón





@tiene_acceso(['administrador'])
def lista_productos(request):
    restaurante = request.user.perfil.restaurante
    productos = restaurante.productos.all()
    return render(request, 'administracion/lista_productos.html', {'productos': productos, 'restaurante': restaurante})




@tiene_acceso(['administrador'])
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            producto = form.save(commit=False)

            # Asignamos el restaurante del usuario
            producto.restaurante = request.user.perfil.restaurante

            producto.save()

            return redirect('lista_productos')

    else:
        form = ProductoForm()

    return render(
        request,
        'administracion/crear_producto.html',
        {'form': form}
    )


@tiene_acceso(['administrador'])
def editar_producto(request, producto_id):
    restaurante = request.user.perfil.restaurante
    producto = restaurante.productos.filter(id=producto_id).first()

    if not producto:
        messages.error(request, "Producto no encontrado.")
        return redirect('lista_productos')

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            form.save()
            return redirect('lista_productos')

    else:
        form = ProductoForm(instance=producto) # Cargamos el producto existente en el formulario

    return render(
        request,
        'administracion/editar_producto.html',
        {'form': form, 'producto': producto}
    )


@tiene_acceso(['administrador'])
def eliminar_producto(request, producto_id):
    restaurante = request.user.perfil.restaurante
    producto = restaurante.productos.filter(id=producto_id).first()

    if not producto:
        messages.error(request, "Producto no encontrado.")
        return redirect('lista_productos')

    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')

    return render(
        request,
        'administracion/eliminar_producto.html',
        {'producto': producto}
    )

@tiene_acceso(['administrador'])
def crear_categoria(request):

    if request.method == 'POST':
        form = CategoriaForm(request.POST)

        if form.is_valid():
            categoria = form.save(commit=False)

            # Asignamos el restaurante del usuario
            categoria.restaurante = request.user.perfil.restaurante

            categoria.save()

            return redirect('lista_productos')

    else:
        form = CategoriaForm()

    return render(
        request,
        'administracion/crear_categoria.html',
        {'form': form}
    )







@tiene_acceso(['administrador'])
def gestion_propinas(request):
    restaurante = request.user.perfil.restaurante

    if request.method == "POST":
        restaurante.propina_activa = 'propina_activa' in request.POST
        restaurante.porcentaje_propina = request.POST.get('porcentaje_propina', 10)
        restaurante.save()
        return redirect('menu_admin')

    return render(request, 'administracion/gestion_propinas.html', {
        "restaurante": restaurante
    })








@tiene_acceso(['encargado'])
def caja(request):
    restaurante = request.user.perfil.restaurante
    # Buscamos la caja abierta
    caja_abierta = Caja.objects.filter(restaurante=restaurante, esta_abierta=True).first()
    
    ventas_actuales = 0
    
    if caja_abierta:
        # Aquí hacemos el cálculo dinámico en tiempo real
        ventas_actuales = Pedido.objects.filter(
            sesion_caja=caja_abierta, 
            esta_pagado=True
        ).aggregate(Sum('total'))['total__sum'] or 0

    return render(request, 'administracion/caja.html', {
        'caja': caja_abierta,
        'ventas_actuales': ventas_actuales # Enviamos el dato al template
    })


@tiene_acceso(['encargado'])
def abrir_caja(request):
    if request.method == "POST":
        restaurante = request.user.perfil.restaurante
        
        # 1. Verificamos si YA existe una caja abierta para este restaurante
        caja_abierta = Caja.objects.filter(restaurante=restaurante, esta_abierta=True).exists()
        
        if caja_abierta:
            messages.warning(request, "Ya existe una caja abierta. Primero cierra la actual.")
            return redirect('caja')
        
        # 2. Si no hay ninguna abierta, creamos una NUEVA
        monto_inicial = request.POST.get('monto_inicial', 0)
        
        Caja.objects.create(
            restaurante=restaurante,
            monto_inicial=monto_inicial,
            saldo_actual=monto_inicial,
            esta_abierta=True,
            fecha_apertura=timezone.now(),
            nombre_cajero=request.user.username # O request.user.perfil.nombre
        )
        
        messages.success(request, "Caja abierta correctamente.")
        return redirect('caja')
    

@tiene_acceso(['encargado'])
def cerrar_caja(request):
    if request.method == "POST":
        restaurante = request.user.perfil.restaurante
        
        # 1. Buscamos la caja abierta
        caja_abierta = Caja.objects.filter(restaurante=restaurante, esta_abierta=True).first()
        
        if not caja_abierta:
            messages.warning(request, "No hay ninguna caja abierta para cerrar.")
            return redirect('caja')
        
        # 2. CALCULAMOS LAS VENTAS (Esto es lo que faltaba)
        # Buscamos todos los pedidos pagados en esta sesión y sumamos su 'total'
        ventas_totales = Pedido.objects.filter(
            sesion_caja=caja_abierta, 
            esta_pagado=True
        ).aggregate(Sum('total'))['total__sum'] or 0
        
        # 3. Cerramos y guardamos los datos finales
        caja_abierta.esta_abierta = False
        caja_abierta.fecha_cierre = timezone.now()
        
        # Guardamos el total calculado para tener auditoría
        # Opcional: caja_abierta.saldo_final = caja_abierta.saldo_actual + ventas_totales
        caja_abierta.saldo_actual += ventas_totales 
        
        caja_abierta.save()
        
        messages.success(request, f"Caja cerrada. Ventas del día: ${ventas_totales}")
        return redirect('caja')
    


@tiene_acceso(['encargado'])
def historial_cajas(request):
    restaurante = request.user.perfil.restaurante
    # Buscamos todas las cajas que ya fueron cerradas
    cajas_pasadas = Caja.objects.filter(restaurante=restaurante, esta_abierta=False).order_by('-fecha_apertura')
    
    return render(request, 'administracion/historial_cajas.html', {
        'cajas': cajas_pasadas
    })

@tiene_acceso(['encargado'])
def detalle_caja(request, caja_id):
    restaurante = request.user.perfil.restaurante

    caja = Caja.objects.filter(id=caja_id, restaurante=restaurante).first()

    if not caja:
        messages.error(request, "Caja no encontrada.")
        return redirect('historial_cajas')

    pedidos = Pedido.objects.filter(sesion_caja=caja, restaurante=restaurante)

    cantidad_pedidos = pedidos.count()

    total_cobrado = pedidos.aggregate(total=Sum('total'))['total'] or 0  # venta + propina, ya cobrado junto
    propinas_totales = pedidos.aggregate(total=Sum('monto_propina'))['total'] or 0
    ventas_sin_propina = total_cobrado - propinas_totales

    return render(request, 'administracion/detalle_historial_caja.html', {
        'caja': caja,
        'pedidos': pedidos,
        'cantidad_pedidos': cantidad_pedidos,
        'ventas_sin_propina': ventas_sin_propina,
        'propinas_totales': propinas_totales,
        'total_recaudado': total_cobrado,
        'restaurante': restaurante
    })









@tiene_acceso(['administrador'])
def gestion_personal(request):
    return render(request, 'administracion/gestion_personal.html')

@tiene_acceso(['administrador'])
def gestionar_garzones(request):
    garzones = Perfil.objects.filter(rol='garzon', restaurante=request.user.perfil.restaurante,)

    return render(request, 'administracion/gestionar_garzones.html', {'garzones': garzones})

@tiene_acceso(['administrador'])
def gestionar_cocineros(request):
    cocineros = Perfil.objects.filter(rol='cocinero', restaurante=request.user.perfil.restaurante,)

    return render(request, 'administracion/gestionar_cocineros.html', {'cocineros': cocineros})

@tiene_acceso(['administrador'])
def gestionar_encargados(request):
    encargados = Perfil.objects.filter(rol='encargado', restaurante=request.user.perfil.restaurante,)

    return render(request, 'administracion/gestionar_encargados.html', {'encargados': encargados})


@tiene_acceso(['administrador'])
def gestionar_operadores(request):
    operadores = Perfil.objects.filter(
        rol='operador',
        restaurante=request.user.perfil.restaurante,
    )

    return render(
        request,
        'administracion/gestionar_operadores.html',
        {'operadores': operadores}
    )






@tiene_acceso(['administrador'])
def agregar_garzon(request):


    if request.method == "POST":
        nombre = request.POST.get("nombre")
        contraseña = request.POST.get("contraseña")

        user = User.objects.create_user(username=nombre, password=contraseña)
        Perfil.objects.create(user=user, rol='garzon', restaurante=request.user.perfil.restaurante)
        
        
        messages.success(request, f"Usuario {nombre} agregado exitosamente.")
        return redirect('gestionar_garzones')
    
    return render(request, 'administracion/gestionar_garzones.html')


@tiene_acceso(['administrador'])
def desactivar_garzon(request, garzon_id):

    garzon = get_object_or_404(
        Perfil,
        id=garzon_id,
        rol='garzon',
        restaurante=request.user.perfil.restaurante
    )

    garzon.activo = False
    garzon.save()

    messages.success(
        request,
        f"Garzón {garzon.user.username} desactivado exitosamente."
    )

    return redirect('gestionar_garzones')


@tiene_acceso(['administrador'])
def activar_garzon(request, garzon_id):

    garzon = get_object_or_404(
        Perfil,
        id=garzon_id,
        rol='garzon',
        restaurante=request.user.perfil.restaurante
    )

    garzon.activo = True
    garzon.save()

    messages.success(
        request,
        f"Garzón {garzon.user.username} activado exitosamente."
    )

    return redirect('gestionar_garzones')


@tiene_acceso(['administrador'])
def reset_password_garzon(request, garzon_id):
    garzon = get_object_or_404(
        Perfil,
        id=garzon_id,
        rol='garzon',
        restaurante=request.user.perfil.restaurante
    )

    if request.method == "POST":
        nueva_password = request.POST.get("password")

        if not nueva_password:
            messages.error(request, "Debes ingresar una contraseña.")
            return redirect('reset_password_garzon', garzon_id=garzon.id)

        user = garzon.user
        user.set_password(nueva_password)
        user.save()

        messages.success(
            request,
            f"Contraseña de {user.username} actualizada correctamente."
        )
        return redirect('gestionar_garzones')

    # Si es GET, mostramos el formulario
    return render(request, 'administracion/reset_password_garzon.html', {
        'garzon': garzon
    })












@tiene_acceso(['administrador'])
def agregar_cocinero(request):


    if request.method == "POST":
        nombre = request.POST.get("nombre")
        contraseña = request.POST.get("contraseña")

        user = User.objects.create_user(username=nombre, password=contraseña)
        Perfil.objects.create(user=user, rol='cocinero', restaurante=request.user.perfil.restaurante)
        
        
        messages.success(request, f"Usuario {nombre} agregado exitosamente.")
        return redirect('gestionar_cocineros')
    
    return render(request, 'administracion/gestionar_cocineros.html')

@tiene_acceso(['administrador'])
def desactivar_cocinero(request, cocinero_id):

    cocinero = get_object_or_404(
        Perfil,
        id=cocinero_id,
        rol='cocinero',
        restaurante=request.user.perfil.restaurante
    )

    cocinero.activo = False
    cocinero.save()

    messages.success(
        request,
        f"Cocinero {cocinero.user.username} desactivado exitosamente."
    )

    return redirect('gestionar_cocineros')

@tiene_acceso(['administrador'])
def activar_cocinero(request, cocinero_id):

    cocinero = get_object_or_404(
        Perfil,
        id=cocinero_id,
        rol='cocinero',
        restaurante=request.user.perfil.restaurante
    )

    cocinero.activo = True
    cocinero.save()

    messages.success(
        request,
        f"Cocinero {cocinero.user.username} activado exitosamente."
    )

    return redirect('gestionar_cocineros')


@tiene_acceso(['administrador'])
def reset_password_cocinero(request, cocinero_id):
    cocinero = get_object_or_404(
        Perfil,
        id=cocinero_id,
        rol='cocinero',
        restaurante=request.user.perfil.restaurante
    )

    if request.method == "POST":
        nueva_password = request.POST.get("password")

        if not nueva_password:
            messages.error(request, "Debes ingresar una contraseña.")
            return redirect('reset_password_cocinero', cocinero_id=cocinero.id)

        user = cocinero.user
        user.set_password(nueva_password)
        user.save()

        messages.success(
            request,
            f"Contraseña de {user.username} actualizada correctamente."
        )
        return redirect('gestionar_cocineros')

    # Si es GET, mostramos el formulario
    return render(request, 'administracion/reset_password_cocinero.html', {
        'cocinero': cocinero
    })








@tiene_acceso(['administrador'])
def agregar_encargado(request):

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        contraseña = request.POST.get("contraseña")

        user = User.objects.create_user(
            username=nombre,
            password=contraseña
        )

        Perfil.objects.create(
            user=user,
            rol='encargado',
            restaurante=request.user.perfil.restaurante
        )

        messages.success(request, f"Usuario {nombre} agregado exitosamente.")
        return redirect('gestionar_encargados')

    return render(request, 'administracion/gestionar_encargados.html')


@tiene_acceso(['administrador'])
def desactivar_encargado(request, encargado_id):

    encargado = get_object_or_404(
        Perfil,
        id=encargado_id,
        rol='encargado',
        restaurante=request.user.perfil.restaurante
    )

    encargado.activo = False
    encargado.save()

    messages.success(
        request,
        f"Encargado {encargado.user.username} desactivado exitosamente."
    )

    return redirect('gestionar_encargados')


@tiene_acceso(['administrador'])
def activar_encargado(request, encargado_id):

    encargado = get_object_or_404(
        Perfil,
        id=encargado_id,
        rol='encargado',
        restaurante=request.user.perfil.restaurante
    )

    encargado.activo = True
    encargado.save()

    messages.success(
        request,
        f"Encargado {encargado.user.username} activado exitosamente."
    )

    return redirect('gestionar_encargados')


@tiene_acceso(['administrador'])
def reset_password_encargado(request, encargado_id):
    encargado = get_object_or_404(
        Perfil,
        id=encargado_id,
        rol='encargado',
        restaurante=request.user.perfil.restaurante
    )

    if request.method == "POST":
        nueva_password = request.POST.get("password")

        if not nueva_password:
            messages.error(request, "Debes ingresar una contraseña.")
            return redirect('reset_password_encargado', encargado_id=encargado.id)

        user = encargado.user
        user.set_password(nueva_password)
        user.save()

        messages.success(
            request,
            f"Contraseña de {user.username} actualizada correctamente."
        )
        return redirect('gestionar_encargados')

    # Si es GET, mostramos el formulario
    return render(request, 'administracion/reset_password_encargado.html', {
        'encargado': encargado
    })








@tiene_acceso(['administrador'])
def agregar_operador(request):

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        contraseña = request.POST.get("contraseña")

        user = User.objects.create_user(
            username=nombre,
            password=contraseña
        )

        Perfil.objects.create(
            user=user,
            rol='operador',
            restaurante=request.user.perfil.restaurante
        )

        messages.success(request, f"Usuario {nombre} agregado exitosamente.")
        return redirect('gestionar_operadores')

    return render(request, 'administracion/gestionar_operadores.html')


@tiene_acceso(['administrador'])
def desactivar_operador(request, operador_id):

    operador = get_object_or_404(
        Perfil,
        id=operador_id,
        rol='operador',
        restaurante=request.user.perfil.restaurante
    )

    operador.activo = False
    operador.save()

    messages.success(
        request,
        f"Operador {operador.user.username} desactivado exitosamente."
    )

    return redirect('gestionar_operadores')


@tiene_acceso(['administrador'])
def activar_operador(request, operador_id):

    operador = get_object_or_404(
        Perfil,
        id=operador_id,
        rol='operador',
        restaurante=request.user.perfil.restaurante
    )

    operador.activo = True
    operador.save()

    messages.success(
        request,
        f"Operador {operador.user.username} activado exitosamente."
    )

    return redirect('gestionar_operadores')


@tiene_acceso(['administrador'])
def reset_password_operador(request, operador_id):
    operador = get_object_or_404(
        Perfil,
        id=operador_id,
        rol='operador',
        restaurante=request.user.perfil.restaurante
    )

    if request.method == "POST":
        nueva_password = request.POST.get("password")

        if not nueva_password:
            messages.error(request, "Debes ingresar una contraseña.")
            return redirect('reset_password_operador', operador_id=operador.id)

        user = operador.user
        user.set_password(nueva_password)
        user.save()

        messages.success(
            request,
            f"Contraseña de {user.username} actualizada correctamente."
        )
        return redirect('gestionar_operadores')

    # Si es GET, mostramos el formulario
    return render(request, 'administracion/reset_password_operador.html', {
        'operador': operador
    })




