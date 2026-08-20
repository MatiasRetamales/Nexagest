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
    print("RESTAURANTE:", restaurante)
    print("CATEGORIAS OBJETO:", categorias)
    print("TOTAL:", categorias.count())
    print(
        "LISTA:",
        list(categorias.values_list("id", "nombre"))
    )
    print("==============================\n")

    return render(
        request,
        "carta/carta_publica.html",
        {
            "restaurante": restaurante,
            "categorias": categorias,
        }
    )