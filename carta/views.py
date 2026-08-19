from django.shortcuts import render, get_object_or_404
from core.models import Caja, Restaurante
from .models import Categoria


def carta_publica(request, restaurante_id):

    restaurante = get_object_or_404(
        Restaurante,
        id=restaurante_id
    )

    categorias = Categoria.objects.filter(
        restaurante=restaurante,
        producto__disponibilidad='disponible'
    ).distinct()

    caja = Caja.objects.filter(
        restaurante=restaurante,
        esta_abierta=True
    ).first()

    return render(
        request,
        'carta/carta_publica.html',
        {
            'restaurante': restaurante,
            'categorias': categorias,
            'caja': caja,
        }
    )