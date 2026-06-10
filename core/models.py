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
    tipo_local = models.CharField(max_length=20, choices=TIPO_LOCAL, default='restaurante')

    def __str__(self):
        return f"{self.nombre} - ({self.estado})"
