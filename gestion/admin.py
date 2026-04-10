from django.contrib import admin
from .models import Cliente, Producto, Pedido, DetallePedido


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'correo', 'telefono', 'creado_en']
    search_fields = ['nombre', 'correo']
    list_per_page = 20


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'stock', 'creado_en']
    search_fields = ['nombre']
    list_filter = ['creado_en']
    list_per_page = 20


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1
    readonly_fields = ['subtotal']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha', 'estado', 'creado_en']
    list_filter = ['estado', 'fecha']
    search_fields = ['cliente__nombre']
    inlines = [DetallePedidoInline]
    list_per_page = 20


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'producto', 'cantidad', 'subtotal']
    list_per_page = 20
