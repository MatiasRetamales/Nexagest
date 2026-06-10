from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_admin, name='menu_admin'),
    
    path('reportes/', views.dashboard, name='dashboard'),
    path('toggle-local/', views.toggle_estado_local, name='url_cambiar_estado'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('administracion/productos/crear/', views.crear_producto, name='crear_producto'),
    path('administracion/productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('administracion/productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]