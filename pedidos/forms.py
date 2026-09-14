from django import forms

from carta.models import Categoria

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto

        fields = [
            "nombre",
            "descripcion",
            "precio",
            "disponibilidad",
            "categoria",
            "imagen",
            "requiere_cocina",
            "disponibilidad",
        ]

        labels = {
            "nombre": "Nombre del producto",
            "descripcion": "Descripción del producto",
            "precio": "Precio ($) SIN PUNTOS NI COMAS",
            "disponibilidad": "¿Está disponible?",
            "categoria": "Categoría",
            "imagen": "Imagen del producto (opcional)",
            "requiere_cocina": "¿Requiere preparación en cocina?",
            "disponibilidad": "Disponibilidad del producto",
        }

        widgets = {
            "descripcion": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Ej: Carne, queso cheddar, tomate y salsa de la casa...",
                }
            ),
            "requiere_cocina": forms.Select(
                choices=[
                    (True, "Sí"),
                    (False, "No"),
                ]
            ),
        }

    def __init__(self, *args, restaurante=None, **kwargs):

        super().__init__(*args, **kwargs)

        if restaurante:
            self.fields["categoria"].queryset = Categoria.objects.filter(
                restaurante=restaurante
            ).order_by("nombre")


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]

        labels = {"nombre": "Nombre de la categoria"}
