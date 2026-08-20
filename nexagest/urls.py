from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mesas import views as vistas_mesas
from pedidos import views as vistas_pedidos
from administracion import views as vistas_administracion
from django.contrib.auth import views as auth_views
from core import views as vistas_core

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    )),

    # Rutas
    path('mesas/', include('mesas.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('cocina/', vistas_pedidos.cocina, name='cocina'),
    path('administracion/', include('administracion.urls')),
    path('carta/', include('carta.urls')),

    # Despacho
    path('despacho/', vistas_core.despacho_usuario, name='despacho'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# =========================================================
# MEDIA LOCAL
# =========================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )