from django import forms
from .models import Producto
from carta.models import Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'disponibilidad', 'categoria']
        
        # Etiquetas amigables para el usuario
        labels = {
            'nombre': 'Nombre del producto',
            'precio': 'Precio ($) SIN PUNTOS NI COMAS',
            'disponibilidad': '¿Está disponible?',
            'categoria': 'Categoría'
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

        labels = {'nombre': 'Nombre de la categoria'}