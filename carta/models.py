
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageOps  # type: ignore[reportMissingImports]


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    restaurante = models.ForeignKey(
        "core.Restaurante",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nombre


def ruta_imagen_producto(instance, filename):
    return (
        f"restaurantes/"
        f"restaurante_{instance.restaurante_id}/"
        f"productos/"
        f"{filename}"
    )


class Producto(models.Model):
    DISPONIBILIDAD = (
        ("disponible", "Disponible"),
        ("no disponible", "No Disponible"),
    )

    nombre = models.CharField(
        max_length=100,
    )

    precio = models.DecimalField(
        max_digits=8,
        decimal_places=0,
    )

    disponibilidad = models.CharField(
        max_length=20,
        choices=DISPONIBILIDAD,
        default="disponible",
    )

    restaurante = models.ForeignKey(
        "core.Restaurante",
        on_delete=models.CASCADE,
        related_name="productos",
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
    )

    imagen = models.ImageField(
        upload_to=ruta_imagen_producto,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        imagen_anterior = None

        # ========================================
        # OBTENER IMAGEN ANTERIOR
        # ========================================

        if self.pk:
            try:
                producto_anterior = Producto.objects.get(
                    pk=self.pk
                )

                imagen_anterior = producto_anterior.imagen

            except Producto.DoesNotExist:
                pass

        # ========================================
        # PROCESAR IMAGEN NUEVA
        # ========================================

        if self.imagen:
            imagen = Image.open(self.imagen)

            # Corregir orientación EXIF
            imagen = ImageOps.exif_transpose(imagen)

            # ========================================
            # CONVERTIR A RGB
            # ========================================

            if imagen.mode in ("RGBA", "LA"):
                fondo = Image.new(
                    "RGB",
                    imagen.size,
                    "white",
                )

                fondo.paste(
                    imagen,
                    mask=imagen.getchannel("A"),
                )

                imagen = fondo

            elif imagen.mode == "P":
                imagen = imagen.convert("RGBA")

                fondo = Image.new(
                    "RGB",
                    imagen.size,
                    "white",
                )

                fondo.paste(
                    imagen,
                    mask=imagen.getchannel("A"),
                )

                imagen = fondo

            else:
                imagen = imagen.convert("RGB")

            # ========================================
            # REDIMENSIONAR
            # ========================================

            max_dimension = 1200

            if (
                imagen.width > max_dimension
                or imagen.height > max_dimension
            ):
                imagen.thumbnail(
                    (
                        max_dimension,
                        max_dimension,
                    ),
                    Image.Resampling.LANCZOS,
                )

            # ========================================
            # CONVERTIR A WEBP
            # ========================================

            buffer = BytesIO()

            imagen.save(
                buffer,
                format="WEBP",
                quality=82,
                method=6,
            )

            buffer.seek(0)

            # ========================================
            # NOMBRE DEL ARCHIVO
            # ========================================

            nombre_archivo = self.imagen.name.rsplit(
                "/",
                1,
            )[-1]

            nombre_archivo = nombre_archivo.rsplit(
                ".",
                1,
            )[0]

            nombre_webp = f"{nombre_archivo}.webp"

            # ========================================
            # REEMPLAZAR IMAGEN
            # ========================================

            self.imagen.save(
                nombre_webp,
                ContentFile(buffer.read()),
                save=False,
            )

        # ========================================
        # GUARDAR PRODUCTO
        # ========================================

        super().save(*args, **kwargs)

        # ========================================
        # ELIMINAR IMAGEN ANTERIOR
        # ========================================

        if (
            imagen_anterior
            and imagen_anterior.name
            and imagen_anterior.name != self.imagen.name
        ):
            try:
                imagen_anterior.delete(
                    save=False
                )

            except Exception:
                pass

    def __str__(self):
        return self.nombre

