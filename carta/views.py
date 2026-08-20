from django.shortcuts import render, get_object_or_404
from core.models import Restaurante
from .models import Categoria
from administracion.models import Caja


def carta_publica(request, restaurante_id):

    restaurante = get_object_or_404(
        Restaurante,
        id=restaurante_id
    )

    categorias = Categoria.objects.filter(
    restaurante=restaurante,
    producto__isnull=False
    ).distinct()


    caja = Caja.objects.filter(
        restaurante=restaurante,
        esta_abierta=True
    ).first()

    caja_abierta = caja is not None
    
    

    return render(
        request,
        'carta/carta_publica.html',
        {
            'restaurante': restaurante,
            'categorias': categorias,
            'caja': caja,
            'caja_abierta': caja_abierta,
        }
    )