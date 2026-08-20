from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    restaurante = models.ForeignKey("core.Restaurante", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


def ruta_imagen_producto(instance, filename):
    return f"restaurantes/restaurante_{instance.restaurante_id}/productos/{filename}"


class Producto(models.Model):
    DISPONIBILIDAD = (
        ("disponible", "Disponible"),
        ("no disponible", "No Disponible"),
    )

    nombre = models.CharField(max_length=100)

    precio = models.DecimalField(max_digits=8, decimal_places=0)

    disponibilidad = models.CharField(
        max_length=20, choices=DISPONIBILIDAD, default="disponible"
    )

    restaurante = models.ForeignKey(
        "core.Restaurante", on_delete=models.CASCADE, related_name="productos"
    )

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    descripcion = models.TextField(blank=True, null=True)

    imagen = models.ImageField(upload_to=ruta_imagen_producto, blank=True, null=True)

    def save(self, *args, **kwargs):

        imagen_anterior = None

        # Si el producto ya existe, buscamos su imagen anterior
        if self.pk:
            try:
                producto_anterior = Producto.objects.get(pk=self.pk)
                imagen_anterior = producto_anterior.imagen

            except Producto.DoesNotExist:
                pass

        # Guardamos primero el producto nuevo
        super().save(*args, **kwargs)

        # Si había una imagen anterior y ahora cambió
        if (
            imagen_anterior
            and imagen_anterior.name
            and imagen_anterior.name != self.imagen.name
        ):
            try:
                imagen_anterior.delete(save=False)

            except Exception:
                pass

    def __str__(self):
        return self.nombre
