from django.db import models

class Restaurante(models.Model):
    ESTADOS = (
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    )

    TIPO_LOCAL = (
        ('restaurante', 'Restaurante'),
        ('local', 'Local'),
    )

    nombre = models.CharField(max_length=100)

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='cerrado'
    )

    tipo_local = models.CharField(
        max_length=20,
        choices=TIPO_LOCAL,
        default='restaurante'
    )

    # =========================
    # PROPINA
    # =========================

    propina_activa = models.BooleanField(
        default=False
    )

    porcentaje_propina = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10
    )

    # =========================
    # PEDIDOS ONLINE
    # =========================

    pedidos_online_activos = models.BooleanField(
        default=False
    )

    acepta_delivery = models.BooleanField(
        default=False
    )

    acepta_pago_local = models.BooleanField(default=True)

    # =========================
    # PAGOS PEDIDOS ONLINE
    # =========================

    acepta_retiro = models.BooleanField(
        default=True
    )

    acepta_pago_transferencia = models.BooleanField(
        default=False
    )

    # =========================
    # DATOS TRANSFERENCIA
    # =========================

    banco_transferencia = models.CharField(
        max_length=100,
        blank=True
    )

    tipo_cuenta_transferencia = models.CharField(
        max_length=50,
        blank=True
    )

    numero_cuenta_transferencia = models.CharField(
        max_length=50,
        blank=True
    )

    titular_transferencia = models.CharField(
        max_length=150,
        blank=True
    )

    rut_transferencia = models.CharField(
        max_length=20,
        blank=True
    )

    correo_transferencia = models.EmailField(
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} - ({self.estado})"