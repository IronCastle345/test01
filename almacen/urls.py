"""
URL configuration for almacen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.parles_dashboard),
    path('cajas/', views.listar_cajas, name='listar_caja'),
    path('cajas/parle/<int:parle_id>/', views.listar_cajas, name='cajas_por_parle'),
    path('cajas/crear', views.registrarCaja, name='crear_caja'),
    path('cajas/eliminar/<int:id>/', views.eliminar_caja, name='eliminar_caja'),
    path('cajas/editar/<int:id>/', views.editar_caja, name='editar_caja'),
    path('cajas/<int:id>/contenido/', views.contenido_caja, name='contenido_caja'),
    path('cajas/<int:id>/agregar-pieza/', views.agregar_pieza, name='agregar_pieza'),
    path('piezas/eliminar/<int:id>/', views.eliminar_pieza, name='eliminar_pieza'),
    path('piezas/editar/<int:id>/', views.editar_pieza, name='editar_pieza'),
    path('parles/', views.parles_dashboard, name='parles_dashboard'),
    path('parles/crear/', views.crear_parle, name='crear_parle'),
    path('parles/<int:id>/actualizar/', views.actualizar_parle, name='actualizar_parle'),
    path('parles/<int:id>/eliminar/', views.eliminar_parle, name='eliminar_parle'),
    path('parles/<int:id>/actualizar-nombre/', views.actualizar_nombre_parle, name='actualizar_nombre_parle'),
]
