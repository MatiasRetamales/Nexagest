from django import forms
from .models import Producto

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