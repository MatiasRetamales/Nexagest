from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def despacho_usuario(request):
    # Si por alguna razón alguien llega aquí sin loguearse, al login
    if not request.user.is_authenticated:
        return redirect('login')

    # Obtenemos el rol desde el perfil
    if hasattr(request.user, 'perfil'):
        rol = request.user.perfil.rol
        
        if rol == 'administrador':
            return redirect('menu_admin')
        elif rol == 'cocinero':
            return redirect('cocina')
        elif rol == 'garzon':
            return redirect('lista_mesas')

    # Si no tiene perfil o el rol es desconocido, al menú principal
    return redirect('menu_admin') # O la que prefieras por defecto