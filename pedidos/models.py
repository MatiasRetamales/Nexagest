from django.db import models
from django.contrib.auth.models import User
from mesas.models import Mesa
from carta.models import Producto


class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Cocina'),
        ('listo', 'Para Entregar'),
        ('entregado', 'Servido'),
        ('cancelado', 'Cancelado'),
    )

    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True)
    garzon = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    esta_pagado = models.BooleanField(default=False)
    enviado_a_cocina = models.DateTimeField(null=True, blank=True)
    total_envios = models.PositiveIntegerField(default=0)
    restaurante = models.ForeignKey("core.Restaurante", on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100, blank=True, null=True)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    propina_aplicada = models.BooleanField(default=False)
    monto_propina = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sesion_caja = models.ForeignKey('administracion.Caja', on_delete=models.SET_NULL, null=True, blank=True)

    def total_con_propina(self):
        return self.total + self.monto_propina

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