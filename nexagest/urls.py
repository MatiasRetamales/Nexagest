from django.contrib import admin
from django.urls import path, include
from mesas import views as vistas_mesas
from pedidos import views as vistas_pedidos
from administracion import views as vistas_administracion
from django.contrib.auth import views as auth_views        # Importar vistas de autenticación internas de Django
from core import views as vistas_core

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Ahora el Login es la raíz (al entrar al sitio, ves el login)
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True   #
    ), name='login'),

    # 2. Mantenemos también /login/ por si acaso
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True   # 
    )),
    
    
    # 2. Las demás rutas se mantienen igual
    path('mesas/', include('mesas.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('cocina/', vistas_pedidos.cocina, name='cocina'),
    path('administracion/', include('administracion.urls')),
    path('carta/', include('carta.urls')),
    
    # Mantenemos el despacho para que después de loguearse se vayan a su lugar
    path('despacho/', vistas_core.despacho_usuario, name='despacho'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]