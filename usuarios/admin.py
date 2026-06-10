from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Perfil

# 1. Registras tu modelo Perfil normal (esto está perfecto)
admin.site.register(Perfil) 

# 2. IMPORTANTE: Desregistrar el User que viene por defecto
admin.site.unregister(User)



# 3. Ahora sí, registras el User con tu configuración personalizada
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Agregamos los filtros (asegúrate que en Perfil existan 'rol' y 'restaurante')
    list_filter = UserAdmin.list_filter + ('perfil__rol', 'perfil__restaurante')
    
    # Mostramos las columnas en la lista principal
    list_display = ('username', 'email', 'get_restaurante', 'is_staff')

    # Método para traer el nombre del restaurante desde el Perfil
    def get_restaurante(self, obj):
        try:
            return obj.perfil.restaurante
        except Perfil.DoesNotExist:
            return "Sin Perfil"
            
    get_restaurante.short_description = 'Restaurante'