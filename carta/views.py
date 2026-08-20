from django.shortcuts import render, get_object_or_404
from core.models import Restaurante
from .models import Categoria
from administracion.models import Caja


def carta_publica(request, restaurante_id):

    print("1 - ENTRANDO A VISTA")

    restaurante = get_object_or_404(
        Restaurante,
        id=restaurante_id
    )

    print("2 - RESTAURANTE:", restaurante)

    categorias = Categoria.objects.filter(
        restaurante=restaurante
    )

    print("3 - CATEGORIAS:", list(categorias))

    caja = Caja.objects.filter(
        restaurante=restaurante,
        esta_abierta=True
    ).first()

    print("4 - CAJA:", caja)

    caja_abierta = caja is not None

    print("5 - ANTES RENDER")

    return render(
        request,
        "carta/carta_publica.html",
        {
            "restaurante": restaurante,
            "categorias": categorias,
            "caja": caja,
            "caja_abierta": caja_abierta,
        }
    )