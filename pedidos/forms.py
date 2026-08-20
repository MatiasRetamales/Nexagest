from django import forms
from .models import Producto
from carta.models import Categoria

class ProductoForm(forms.ModelForm):

    class Meta:

        model = Producto

        fields = [
            'nombre',
            'descripcion',
            'precio',
            'disponibilidad',
            'categoria',
            'imagen',
        ]

        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción del producto',
            'precio': 'Precio ($) SIN PUNTOS NI COMAS',
            'disponibilidad': '¿Está disponible?',
            'categoria': 'Categoría',
            'imagen': 'Imagen del producto (opcional)',
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ej: Carne, queso cheddar, tomate y salsa de la casa...'
            })
        }


    def __init__(self, *args, restaurante=None, **kwargs):

        super().__init__(*args, **kwargs)

        if restaurante:

            self.fields['categoria'].queryset = Categoria.objects.filter(
                restaurante=restaurante
            ).order_by('nombre')

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

        labels = {'nombre': 'Nombre de la categoria'}