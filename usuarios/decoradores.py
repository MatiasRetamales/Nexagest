from django.shortcuts import redirect
from django.contrib import messages

# --- DECORADOR PARA COCINERO ---
def solo_cocinero(view_func):
    def wrap(request, *args, **kwargs):
        # 1. ¿Está logueado?
        if not request.user.is_authenticated:
            return redirect('/login/')

        # 2. ¿Tiene perfil y el rol correcto? 
        # (El administrador también puede entrar a ver)
        if hasattr(request.user, 'perfil'):
            if request.user.perfil.rol == 'cocinero' or request.user.perfil.rol == 'administrador':
                return view_func(request, *args, **kwargs)
        
        messages.error(request, "Acceso denegado: Solo Cocina.")
        return redirect('/login/') # Si no es cocinero, quizás es garzón, lo mandamos allá
    return wrap

# --- DECORADOR PARA GARZÓN ---
def solo_garzon(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')

        if hasattr(request.user, 'perfil'):
            if request.user.perfil.rol == 'garzon' or request.user.perfil.rol == 'administrador':
                return view_func(request, *args, **kwargs)
        
        messages.error(request, "Acceso denegado: Solo Garzones.")
        return redirect('/login/') # Si no es garzón, quizás es cocinero, lo mandamos allá
    return wrap

# --- DECORADOR PARA ADMINISTRADOR ---
def solo_admin_restaurante(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')

        if hasattr(request.user, 'perfil'):
            if request.user.perfil.rol == 'administrador':
                return view_func(request, *args, **kwargs)
        
        messages.error(request, "Acceso denegado: Solo Administradores.")
        return redirect('/login/') # Si no es admin, lo mandamos al admin para que vea su perfil o lo que corresponda
    return wrap


