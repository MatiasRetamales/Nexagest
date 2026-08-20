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

    print("\n==============================")
    print("RESTAURANTE ID:", restaurante.id)
    print("TOTAL CATEGORIAS:", categorias.count())

    for categoria in categorias:
        print(
            "CATEGORIA:",
            categoria.nombre,
            "| ID:",
            categoria.id,
            "| RESTAURANTE ID:",
            categoria.restaurante.id
        )

    print("==============================")

    print("ANTES DE CAJA")

    caja = Caja.objects.filter(
        restaurante=restaurante,
        esta_abierta=True
    ).first()

    print("DESPUES DE CAJA")
    print("CAJA:", caja)

    caja_abierta = caja is not None

    print("ANTES DEL RENDER")

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