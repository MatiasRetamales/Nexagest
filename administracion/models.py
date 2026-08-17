from django.db import models

# Create your models here.
class Caja(models.Model):
    restaurante = models.ForeignKey('core.Restaurante', on_delete=models.CASCADE)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    nombre_cajero = models.CharField(max_length=100, null=True, blank=True)
    esta_abierta = models.BooleanField(default=False)
    efectivo_contado = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True )
    diferencia_caja = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True )

    def __str__(self):
        return f"Caja de {self.restaurante.nombre} - Saldo: {self.saldo_actual}"