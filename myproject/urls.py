"""
Configuración de URLs Globales del Proyecto.
Este archivo es el 'Portero' del sitio. Decide qué gran sección del sitio 
va a manejar cada petición (Admin, Cuentas o la App de Gestión).
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Panel de administración predeterminado de Django.
    path('admin/', admin.site.urls),
    
    # Redirección: Si el usuario entra a la dirección raíz (vacía), 
    # automáticamente lo enviamos a la pestaña de pedidos.
    path('', RedirectView.as_view(url='/pedidos/', permanent=False)),
    
    # Sistema de Autenticación: Maneja las rutas de Login y Logout.
    path('cuentas/', include('django.contrib.auth.urls')),
    
    # Rutas de la Aplicación: Incluimos todas las direcciones que 
    # programamos dentro de la carpeta 'gestion'.
    path('', include('gestion.urls')),
]
