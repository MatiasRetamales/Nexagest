from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta # Necesitamos estas para los cálculos
from django.contrib import messages
from pedidos.models import Pedido
from core.models import Restaurante
from usuarios.decoradores import solo_admin_restaurante
from django.shortcuts import render, redirect
from pedidos.forms import ProductoForm



@solo_admin_restaurante
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
        estado="pagado"
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




@solo_admin_restaurante
def menu_admin(request):
    # 1. Buscamos el restaurante en la base de datos
    restaurante = request.user.perfil.restaurante
    
    # 2. Lo metemos en el diccionario de contexto
    context = {
        'restaurante': restaurante
    }
    
    # 3. Lo pasamos al render
    return render(request, 'administracion/menu_admin.html', context)


@solo_admin_restaurante
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


@solo_admin_restaurante
def lista_productos(request):
    restaurante = request.user.perfil.restaurante
    productos = restaurante.productos.all()
    return render(request, 'administracion/lista_productos.html', {'productos': productos, 'restaurante': restaurante})




@solo_admin_restaurante
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


@solo_admin_restaurante
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


@solo_admin_restaurante
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