"""
URLs de la aplicación de gestión de pedidos.
Este archivo es como el 'mapa' del sitio web. Aquí definimos qué palabra 
en la dirección del navegador (URL) activa qué función en views.py.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard: La página inicial con las estadísticas.
    path('dashboard/', views.dashboard, name='dashboard'),

    # ============================================================
    #  RUTAS PARA CLIENTES
    # ============================================================
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    
    # <int:pk> indica que pasamos el ID (Primary Key) del cliente por la URL.
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
    path('clientes/<int:pk>/detalle/', views.cliente_list, name='cliente_detail'), # Nota: Enlazado para ejemplo.

    # ============================================================
    #  RUTAS PARA PRODUCTOS
    # ============================================================
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/nuevo/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),

    # ============================================================
    #  RUTAS PARA PEDIDOS
    # ============================================================
    path('pedidos/', views.pedido_list, name='pedido_list'),
    path('pedidos/nuevo/', views.pedido_create, name='pedido_create'),
    path('pedidos/<int:pk>/editar/', views.pedido_update, name='pedido_update'),
    path('pedidos/<int:pk>/eliminar/', views.pedido_delete, name='pedido_delete'),
    
    # Detalle del pedido: Donde agregamos productos al 'carrito'.
    path('pedidos/<int:pk>/detalle/', views.pedido_detail, name='pedido_detail'),
    path('pedidos/detalle/<int:pk>/eliminar/', views.detalle_delete, name='detalle_delete'),

    # ============================================================
    #  RUTAS DE EXPORTACIÓN (REPORTES)
    # ============================================================
    path('export/pedidos/pdf/', views.export_pedidos_pdf, name='export_pedidos_pdf'),
    path('export/pedidos/excel/', views.export_pedidos_excel, name='export_pedidos_excel'),
    path('export/clientes/excel/', views.export_clientes_excel, name='export_clientes_excel'),
    path('export/productos/excel/', views.export_productos_excel, name='export_productos_excel'),

    # ============================================================
    #  AUTENTICACIÓN (REGISTRO PÚBLICO)
    # ============================================================
    path('registro/', views.registro_usuario, name='registro'),

    # ============================================================
    #  API REST (ENDPOINTS JSON)
    # ============================================================
    path('api/clientes/', views.api_cliente_list, name='api_cliente_list'),
    path('api/productos/', views.api_producto_list, name='api_producto_list'),
    path('api/docs/', views.api_docs, name='api_docs'),
    path('docs/', views.api_docs, name='api_docs_short'),
    path('api/pedidos/<int:pk>/delete/', views.api_pedido_delete, name='api_pedido_delete'),
]
