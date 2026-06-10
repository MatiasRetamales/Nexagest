from django.db import models

class Mesa(models.Model):
    ESTADOS = [
        ('libre', 'Libre'),
        ('ocupada', 'Ocupada'),
    ]
    numero = models.PositiveIntegerField(unique=False)
    activa = models.BooleanField(default=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='libre')
    restaurante = models.ForeignKey('core.Restaurante', on_delete=models.CASCADE, related_name='mesas')

    def __str__(self):
        return f"Mesa {self.numero}"