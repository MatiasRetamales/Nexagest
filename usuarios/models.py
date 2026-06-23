from django.db import models
from django.contrib.auth.models import User # Importa el modelo User de Django

class Perfil(models.Model):

    ROLES = (
        ('garzon', 'Garzón'),
        ('cocinero', 'Cocinero'),
        ('administrador', 'Administrador'),
        ('encargado', 'Encargado'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User
    rol = models.CharField(max_length=20, choices=ROLES)
    nombre_usuario = models.CharField(max_length=50)
    restaurante = models.ForeignKey('core.Restaurante', on_delete=models.CASCADE, related_name='perfiles')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
    

