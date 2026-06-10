from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    restaurante = models.ForeignKey("core.Restaurante", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre




class Producto(models.Model):
    DISPONIBILIDAD = [
        ('disponible', 'Disponible'),
        ('no disponible', 'No Disponible'),
    ]
    
  
    
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=0)  # sin decimales
    disponibilidad = models.CharField(max_length=20, choices=DISPONIBILIDAD, default='disponible')
    restaurante = models.ForeignKey("core.Restaurante", on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre