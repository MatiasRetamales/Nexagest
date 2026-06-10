return HttpResponse → “Toma texto plano y muéstralo, se usa para no utilizar plantillas aun html”.

return render → “Toma una plantilla HTML y complétala con datos, renderiza la misma pagina”.

return redirect "simplemente redirije a otra URL" 



✔ value = lo que recibe Django
✔ name = etiqueta para agrupar datos
✔ getlist = obtener todos los valores que tengan el MISMO name
✔ get = obtener un único valor del name









Para TRAER OBJETOS DE LA BASE DE DATOS (MODELOS)

🔹 Traer un solo registro
Pedido.objects.first()      # Primer pedido (ID más bajo)
Pedido.objects.last()       # Último pedido (ID más alto)
Pedido.objects.get(id=10)   # Pedido con ID exacto

🔹 Filtrar (traer varios registros)
Pedido.objects.filter(estado='pendiente')     # Filtra por estado
Pedido.objects.filter(mesa__numero=1)         # Filtra pedidos de la mesa 1
Pedido.objects.filter(garzon__username='Matias')
Pedido.objects.filter(fecha__date='2025-11-16')

🔹 Excluir
Pedido.objects.exclude(estado='entregado')

🔹 Ordenar
Pedido.objects.order_by('fecha')      # Ascendente
Pedido.objects.order_by('-fecha')     # Descendente

🔹 Contar
Pedido.objects.count()                # Cantidad total de pedidos
Pedido.objects.filter(estado='pendiente').count()

🔹 Crear registros
Pedido.objects.create(mesa=mesa_obj, garzon=user_obj)

🔹 Actualizar un objeto
pedido = Pedido.objects.get(id=36)
pedido.estado = 'entregado'
pedido.save()

🔹 Borrar un registro
Pedido.objects.get(id=36).delete()

🔹 Recorrer todos
for p in Pedido.objects.all():
    print(p.id, p.estado)

Modelo.objects.get(...)       # Trae 1
Modelo.objects.filter(...)    # Trae muchos
Modelo.objects.create(...)    # Crea
Modelo.objects.update(...)    # Actualiza varios
Modelo.objects.all()          # Trae todos
Modelo.objects.delete()       # Borra vario