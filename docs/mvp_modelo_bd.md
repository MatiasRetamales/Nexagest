# Modelo de Base de Datos - MVP Nexagest (Restaurantes)

## Resumen
Documento de diseño de las tablas y relaciones para el MVP:
- Usuarios (auth_user + Perfil)
- Mesas
- Productos
- Pedidos
- PedidoItem

---

## Tablas

### Usuario (usado: auth_user)
Campos principales: id, username, password, email, first_name, last_name, is_active, date_joined.

### Perfil
- user: OneToOneField(User)
- rol: CharField(choices=['dueno','garzon','cocinero'])
- nombre_visible: CharField (opcional)
- restaurante: FK (opcional para multi-sucursal futura)

### Mesa
- id
- numero: IntegerField (unique)
- capacidad: SmallIntegerField
- ocupada: BooleanField
- descripcion: CharField (opcional)

### Producto
- id
- nombre: CharField
- precio: DecimalField
- categoria: CharField (opcional)
- disponible: BooleanField

### Pedido
- id
- mesa: FK -> Mesa (nullable para locales sin mesa)
- garzon: FK -> User (quien crea el pedido)
- estado: CharField(choices: pendiente, en_preparacion, listo, entregado, cancelado)
- total: DecimalField (calculado o almacenado)
- creado_en: DateTimeField(auto_now_add=True)
- actualizado_en: DateTimeField(auto_now=True)

### PedidoItem
- id
- pedido: FK -> Pedido (related_name='items')
- producto: FK -> Producto
- cantidad: PositiveIntegerField
- precio_unitario: DecimalField (copiado del Producto al crear)
- subtotal: DecimalField (cantidad * precio_unitario)
- notas: CharField (opcional)

---

## Relaciones clave
- Perfil 1:1 -> User
- Mesa 1:N -> Pedido (una mesa puede tener muchos pedidos en el tiempo)
- Pedido 1:N -> PedidoItem (un pedido contiene múltiples ítems)
- Producto 1:N -> PedidoItem

---

## Notas
- Mantener esta versión como esquema inicial. Cualquier cambio grande se documenta aquí antes de tocar código.
- Archivo: docs/mvp_modelo_bd.md
