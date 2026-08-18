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
            'categoria'
        ]

        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción del producto',
            'precio': 'Precio ($) SIN PUNTOS NI COMAS',
            'disponibilidad': '¿Está disponible?',
            'categoria': 'Categoría'
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ej: Carne, queso cheddar, tomate y salsa de la casa...'
            })
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

        labels = {'nombre': 'Nombre de la categoria'}