from django.shortcuts import redirect
from django.contrib import messages

def tiene_acceso(roles_permitidos):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')

            perfil = getattr(request.user, 'perfil', None)

            if not perfil:
                return redirect('/login/')

            rol = perfil.rol.strip().lower()

            # admin siempre entra
            if rol == 'administrador':
                return view_func(request, *args, **kwargs)

            # otros roles controlados por lista
            if rol in roles_permitidos:
                return view_func(request, *args, **kwargs)

            messages.error(request, "Acceso denegado")
            return redirect('/login/')

        return wrap
    return decorator
