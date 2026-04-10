"""
Script para cargar datos de prueba en la base de datos.
Ejecutar con: python manage.py shell < seed_data.py
O con: python seed_data.py (desde la carpeta raíz del proyecto)
"""
import os
import django
import sys

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from gestion.models import Cliente, Producto, Pedido, DetallePedido
from datetime import date, timedelta
from decimal import Decimal

print("Cargando datos de prueba...")

# Limpiar datos existentes (opcional)
DetallePedido.objects.all().delete()
Pedido.objects.all().delete()
Cliente.objects.all().delete()
Producto.objects.all().delete()

# --- CLIENTES ---
clientes = [
    Cliente(nombre="María García López", correo="maria.garcia@email.com", direccion="Calle 45 # 23-10, Bogotá", telefono="300 123 4567"),
    Cliente(nombre="Carlos Rodríguez", correo="carlos.rodriguez@email.com", direccion="Carrera 7 # 15-30, Medellín", telefono="311 234 5678"),
    Cliente(nombre="Ana Martínez", correo="ana.martinez@email.com", direccion="Avenida 6 # 12-45, Cali", telefono="322 345 6789"),
    Cliente(nombre="Pedro Sánchez", correo="pedro.sanchez@email.com", direccion="Calle 100 # 50-20, Barranquilla", telefono="333 456 7890"),
    Cliente(nombre="Lucía Hernández", correo="lucia.hernandez@email.com", direccion="Carrera 15 # 80-15, Bogotá", telefono="315 567 8901"),
]
for c in clientes:
    c.save()
print(f"  ✅ {len(clientes)} clientes creados")

# --- PRODUCTOS ---
productos = [
    Producto(nombre="Laptop Dell Inspiron 15", precio=Decimal("2500000.00"), stock=15),
    Producto(nombre="Mouse Inalámbrico Logitech", precio=Decimal("85000.00"), stock=50),
    Producto(nombre="Teclado Mecánico RGB", precio=Decimal("250000.00"), stock=30),
    Producto(nombre="Monitor LG 24 pulgadas", precio=Decimal("850000.00"), stock=10),
    Producto(nombre="Auriculares Sony WH-1000XM4", precio=Decimal("1200000.00"), stock=8),
    Producto(nombre="Webcam Full HD 1080p", precio=Decimal("180000.00"), stock=25),
    Producto(nombre="Disco Duro Externo 1TB", precio=Decimal("220000.00"), stock=20),
    Producto(nombre="Hub USB-C 7 puertos", precio=Decimal("120000.00"), stock=40),
    Producto(nombre="Silla Ergonómica Office", precio=Decimal("650000.00"), stock=5),
    Producto(nombre="Tablet Samsung Galaxy A8", precio=Decimal("980000.00"), stock=12),
]
for p in productos:
    p.save()
print(f"  ✅ {len(productos)} productos creados")

# --- PEDIDOS ---
pedidos_data = [
    (clientes[0], date.today() - timedelta(days=15), 'Entregado'),
    (clientes[1], date.today() - timedelta(days=7), 'Enviado'),
    (clientes[2], date.today() - timedelta(days=3), 'Pendiente'),
    (clientes[3], date.today() - timedelta(days=1), 'Pendiente'),
    (clientes[4], date.today(), 'Pendiente'),
    (clientes[0], date.today() - timedelta(days=30), 'Entregado'),
    (clientes[2], date.today() - timedelta(days=10), 'Enviado'),
]

pedidos = []
for cliente, fecha, estado in pedidos_data:
    p = Pedido(cliente=cliente, fecha=fecha, estado=estado)
    p.save()
    pedidos.append(p)
print(f"  ✅ {len(pedidos)} pedidos creados")

# --- DETALLES DE PEDIDO ---
detalles_data = [
    (pedidos[0], productos[0], 1),
    (pedidos[0], productos[1], 2),
    (pedidos[0], productos[2], 1),
    (pedidos[1], productos[3], 1),
    (pedidos[1], productos[5], 1),
    (pedidos[2], productos[4], 1),
    (pedidos[3], productos[6], 2),
    (pedidos[3], productos[7], 3),
    (pedidos[4], productos[8], 1),
    (pedidos[4], productos[9], 1),
    (pedidos[5], productos[1], 5),
    (pedidos[5], productos[7], 2),
    (pedidos[6], productos[0], 1),
    (pedidos[6], productos[2], 2),
]

for pedido, producto, cantidad in detalles_data:
    d = DetallePedido(pedido=pedido, producto=producto, cantidad=cantidad)
    d.save()
print(f"  ✅ {len(detalles_data)} detalles de pedido creados")

print("\n🎉 Datos de prueba cargados exitosamente!")
print(f"   👥 Clientes: {Cliente.objects.count()}")
print(f"   📦 Productos: {Producto.objects.count()}")
print(f"   🛒 Pedidos: {Pedido.objects.count()}")
print(f"   📋 Detalles: {DetallePedido.objects.count()}")
