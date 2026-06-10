from django.db import models
from django.contrib.auth.models import User
from mesas.models import Mesa
from carta.models import Producto


class Pedido(models.Model):
    ESTADOS = (
    ('pendiente', 'Pendiente'),
    ('en_preparacion', 'En Cocina'),  # Cambiamos solo lo que ve el garzón
    ('listo', 'Para Entregar'),      # El código sigue buscando 'listo'
    ('entregado', 'Servido'),        # Pero el garzón ve 'Servido'
    ('cancelado', 'Cancelado'),
    ('pagado', 'Pagado'),            
)
    

    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True) # Relación con Mesa
    garzon = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # Relación con Usuario (Garzón)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    enviado_a_cocina = models.DateTimeField(null=True, blank=True)
    total_envios = models.PositiveIntegerField(default=0) #total de envios a cocina para este pedido
    restaurante = models.ForeignKey("core.Restaurante", on_delete=models.CASCADE) # Relación con Restaurante
    nombre_cliente = models.CharField(max_length=100, blank=True, null=True) # Nombre del cliente para pedidos sin mesa
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.numero}"
    
    

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="items", on_delete=models.CASCADE) # Este Item pertenece a UN pedido Y un Pedido puede tener MUCHOS items (Relación Uno → Muchos)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) # Este Item pertenece a UN producto Y un Producto puede estar en MUCHOS items (Relación Uno → Muchos)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.TextField(blank=True, null=True)
    enviado_a_cocina = models.BooleanField(default=False)
    numero_envio = models.PositiveIntegerField(default=0) # Número de veces que este item ha sido enviado a cocina

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"